import MySQLdb
import json
import os
import shutil
import rpy2.robjects as robjects
import time
from rpy2.robjects.packages import importr
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from public_function import (CE, SPECIES, STAT_METHOD, ADJUST_P,
                             NAME_MAPPING, dic2string, get_url,
                             check_log_file, RESULT_FILE_NAME, _, Q,
                             BASE_MSG, BASE_MSG_ERROR, URL, MEDIA_ROOT)


def get_project_info(q_queue, q_files, q_user, q_project, system='linux'):
    """
    :param q_queue: query project queue
    :param q_files: query upload file
    :param q_user: query users
    :param q_project: query project
    :param system: linux/windows
    :return: one paras and related files if exist
    """
    db = MySQLdb.connect(host=_['host'], user=_['user'], passwd=_['passwd'], db=_['db'], port=_['port'])
    try:
        paras = ''  # a string comes from json.dumps(a_dic)
        project_id = -1
        user_id = -1
        pro = {'name': '', 'id': -1}  # project
        with db.cursor() as cursor:
            cursor.execute(query=q_queue)
            one_queue = cursor.fetchone()
            print('####', 'one_queue', one_queue, '\n')
            if one_queue:
                # project_queue_id, user_id, project_id, paras, status, submit_time, start_time, end_time = one_queue
                project_queue_id, user_id, paras, status, submit_time, project_id, end_time, start_time = one_queue
                print(paras)
                if system == 'windows':
                    # paras = paras.replace('\\', '/')
                    paras = paras.replace('/tmp/metdna-upload', 'D://tmp//metdna-upload')
        with db.cursor() as cursor:
            q_files = q_files.format(id=int(project_id))
            cursor.execute(query=q_files)
            files = cursor.fetchall()
        with db.cursor() as cursor:
            q_user = q_user.format(id=int(user_id))
            cursor.execute(query=q_user)
            user = cursor.fetchone()
        with db.cursor() as cursor:
            q_project = q_project.format(id=int(project_id))
            cursor.execute(query=q_project)
            project = cursor.fetchone()
            if project:
                pro['id'] = project[0]
                pro['name'] = project[2]
        # print(files)
        # print(user)
        if paras and len(files) != 0 and len(user) != 0:
            # print('i am here')
            return {'paras': json.loads(paras), 'files': files,
                    'user': user, 'pro': pro}
        else:
            return {'paras': {}, 'files': [], 'user': [], 'pro': pro}
    except:
        with open('db.log', 'a') as f:
            f.write('open db error, project id {}, {}'.format(-1, time.ctime()) + '\n')
        return {'paras': {}, 'files': [], 'user': [], 'pro': {}}
    finally:
        db.close()


def convert_paras(paras, p_files, system='linux'):
    """
    get parameters fo MetDNA and copy 'sample info' file if needed
    :param paras: all parameters of this project, {}
    :param p_files: all uploaded files of this project, []
    :param system: windows/linux
    :return: paras for R package - MetDNA
    """
    new_paras = {}
    # print('##----in function of convert_paras----##\n')
    # print(p_files)
    if paras:
        # ms1_data = UploadFile.objects.filter(project_id=project.id, file_type='ms1_data')
        # sample_info = UploadFile.objects.filter(project_id=project.id, file_type='sample_info')
        # import pdb
        # pdb.set_trace()
        # paras = json.loads(paras)
        # print(type(paras))
        _pol = paras['polarity'].lower()
        for key in paras.keys():
            if str(key) == 'ce':
                paras[key] = CE[paras[key]]
            elif str(key) == 'species':
                paras[key] = SPECIES[paras[key]]
            elif str(key) == 'statMethod':
                paras[key] = STAT_METHOD[paras[key]]
            elif str(key) == 'polarity' or str(key) == 'lcType':
                paras[key] = paras[key].lower()
            elif str(key) == 'adjustP':
                paras[key] = ADJUST_P[paras[key]]
            elif str(key) == 'pCutoff':
                paras[key] = float(paras[key])
            new_paras[NAME_MAPPING[key]] = str(paras[key])
        new_paras['ms1.data.pos'] = ''
        new_paras['ms1.data.neg'] = ''
        new_paras['sample.info.pos'] = [i[2] for i in p_files if i[3] == 'sample_info'][0]
        new_paras['sample.info.neg'] = new_paras['sample.info.pos']  # same sample info file name
        new_paras['pos.path'] = os.path.join(paras['path'], 'POS')
        new_paras['neg.path'] = os.path.join(paras['path'], 'NEG')
        # print(new_paras)
        del new_paras['path']
        if system == 'windows':
            new_paras['pos.path'] = new_paras['pos.path'].replace('\\', '//')
            new_paras['neg.path'] = new_paras['neg.path'].replace('\\', '//')
        sample_info_path_pos = ''
        sample_info_path_neg = ''
        print(_pol)
        if _pol == 'positive' or _pol == 'both':
            new_paras['ms1.data.pos'] = [i[2] for i in p_files if (i[3] == 'ms1_data' and i[-1] == 'POS')][0]
            sample_info_path_pos = os.path.join(new_paras['pos.path'], new_paras['sample.info.pos'])
        if _pol == 'negative' or _pol == 'both':
            new_paras['ms1.data.neg'] = [i[2] for i in p_files if (i[3] == 'ms1_data' and i[-1] == 'NEG')][0]
            sample_info_path_neg = os.path.join(new_paras['neg.path'], new_paras['sample.info.neg'])
        print(sample_info_path_neg, sample_info_path_pos)
        if sample_info_path_pos and sample_info_path_neg:  # both mode
            if os.path.exists(sample_info_path_pos):
                shutil.copy(sample_info_path_pos, sample_info_path_neg)
            elif os.path.exists(sample_info_path_neg):
                shutil.copy(sample_info_path_neg, sample_info_path_pos)
        # path = os.path.join(settings.MEDIA_ROOT, user.username, project.project_hash)
        # new_paras['path'] = path
        # new_paras['ms1.data'] = ms1_data[0].file_name
        # new_paras['sample.info'] = sample_info[0].file_name

        return dic2string(new_paras)


def call_metdna(paras):
    """

    :param paras:
    :return:
    """
    importr('MetDNA')
    rcode = 'MetDNA(' + paras + ')'
    # print(type(paras))
    # print(paras)
    # para_temp = paras.split(', ')
    # print(rcode)
    robjects.r(rcode)
    # update_sent = update.format(status='done', id=project_queue_id)
    # cursor.execute(update_sent)


def send_mail(to_email, subject, message,
              server='mail.cstnet.cn',
              from_email='metdna@sioc.ac.cn'):
    # https://stackoverflow.com/a/47571812/2803344
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email)
    metdna_logo = make_msgid()
    zhulab_logo = make_msgid()

    msg.add_alternative(message.format(metdna_logo=metdna_logo[1:-1],
                                       zhulab_logo=zhulab_logo[1:-1]),
                        subtype='html')
    print('current dir: ', os.getcwd())
    print('current dir: ', os.path.dirname(os.path.abspath(__file__)))
    current_script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_script_dir)
    with open(r'/code/logo-mini.png', 'rb') as img:
        msg.get_payload()[0].add_related(img.read(), 'image', 'png', cid=metdna_logo)
    with open(r'/code/zhulab_mini_logo.png', 'rb') as img:
        msg.get_payload()[0].add_related(img.read(), 'image', 'png', cid=zhulab_logo)
    server = smtplib.SMTP_SSL(server, 465)
    # server = smtplib.SMTP(server)
    # server.set_debuglevel(1)
    with open('./metdna_email_passwd.secret') as f:
        pw = f.read.strip()
    server.login(from_email, pw)
    server.send_message(msg)
    server.quit()
    # print('successfully sent the mail.')


def update_db_status(db_log_in, project_id, status, query):
    """
    update database status when started or finished analysis, doing/done/error
    :param db_log_in: log in information
    :param project_id:
    :param status: status depends on log file
    :param query: query statement to update db
    :return:
    """
    _ = db_log_in
    db = MySQLdb.connect(host=_['host'], user=_['user'], passwd=_['passwd'], db=_['db'])
    try:
        with db.cursor() as cursor:
            update_status = query.format(project_id=project_id, status=status)
            # print(update_status)
            cursor.execute(query=update_status)
            db.commit()
    except:
        with open('db.log', 'a') as f:
            f.write('open db error, project id {}, {}'.format(project_id, time.ctime()) + '\n')
    finally:
        db.close()


counter = 0
while counter == 0:
    # counter += 1
    time.sleep(5)
    q_results = get_project_info(q_queue=Q['q_pro_queue'],
                                 q_files=Q['q_files'],
                                 q_user=Q['q_user'],
                                 q_project=Q['q_pro'])
    # print(q_results)
    paras = q_results['paras']  # raw parameters come from user input, a dic
    if paras:
        is_active = q_results['user'][11]
        user_email = q_results['user'][9]
        current_project = q_results['pro']
        # create results dir: project_root_dir/results
        p_root_dir = paras['path']
        results_dir = os.path.join(p_root_dir, 'results')
        if not os.path.exists(results_dir):
            os.mkdir(results_dir)
        try:
            if is_active == 1:
                pol = paras['polarity'].lower()
                input_file = q_results['files']
                r_paras = convert_paras(paras=paras,
                                        p_files=input_file)
                print('#-----------r_paras\n')
                print(r_paras)
                # print(q_results['paras'])
                update_db_status(db_log_in=_, project_id=current_project['id'],
                                 status='doing', query=Q['update_before_analysis'])

                call_metdna(paras=r_paras)
                time.sleep(10)
                print('#before get url', paras)
                url = get_url(root_dir=paras['path'], pol=pol, result_fn=RESULT_FILE_NAME)
                # log_path = url['log_path']
                print(url)
                status = check_log_file(url=url)
                print(status)
                # result_file_status = check_result_file(local_url, file_name=RESULT_FILE_NAME)
                update_db_status(db_log_in=_, project_id=current_project['id'],
                                 status=status['result_status'], query=Q['update_after_analysis'])
                if status['result_status'] == 'done' and status['exist_status'] == 'exist':
                    # get all result name, both mode will get
                    # ['results_pos.tar.gz', 'results_neg.tar.gz', 'results_pathway.tar.gz']
                    a_r_names = [i.split('/')[-1] for i in url['result_url'].split(', ')]
                    a_r_urls = ', '.join([os.path.join(results_dir, i) for i in a_r_names])
                    a_r_urls = a_r_urls.replace(MEDIA_ROOT, URL)
                    base_msg = BASE_MSG.format(project_name=current_project['name'],
                                               url=a_r_urls,
                                               metdna_logo='cid:{metdna_logo}',
                                               zhulab_logo='cid:{zhulab_logo}')
                    # print(message)
                    # print(is_active, user_email)
                    send_mail(to_email=[user_email, 'xiongxin@sioc.ac.cn'],
                              subject='Project {} has done!'.format(current_project['name']),
                              message=base_msg)
                else:
                    raise Exception('status error!')
        except:
            print('error occurred!!!')
            update_db_status(db_log_in=_, project_id=current_project['id'],
                             status='error', query=Q['update_after_analysis'])
            base_msg = BASE_MSG_ERROR.format(project_name=current_project['name'],
                                             metdna_logo='cid:{metdna_logo}',
                                             zhulab_logo='cid:{zhulab_logo}')
            send_mail(to_email=[user_email, 'xiongxin@sioc.ac.cn'],
                      subject='Project {} has error!'.format(current_project['name']),
                      message=base_msg)
