import os
import shutil
# URL = 'http://localhost:8024/media'
URL = 'http://metdna.zhulab.cn/media'  # web url
MEDIA_ROOT = '/mnt/data/metdna-upload'  # local path

CE = {"10": "10", "15": "15", "20": "20", "25": "25",
      "30": "30", "35": "35", u"35\xb115": "35,15", "40": "40", "45": "45",
      "50": "50", "55": "55", "60": "60", "65": "65", "70": "70"}

SPECIES = {"Homo sapiens (human)":  "hsa", "Mus musculus (mouse)": "mmu",
           "Rattus norvegicus (rat)": "rat", "Bos taurus (cow)": "bta",
           "Drosophila melanogaster (fruit fly)": "dme",
           "Gallus gallus (chicken)": "gga", "Danio rerio (zebrafish)": "dre",
           "Caenorhabditis elegans (nematode)": "cel",
           "Saccharomyces cerevisiae (yeast)": "sce",
           "Arabidopsis thaliana (thale cress)": "ath",
           "Schistosoma mansoni": "smm",
           "Plasmodum falciparum 3D7 (Malaria)": "pfa",
           "Trypanosoma brucei": "tbr",
           "Escherichia coli K-12 MG1655": "eco",
           "Pseudomonas putida KT2440": "ppu", "Synechococcus elongatus": "syf"}

STAT_METHOD = {'Student t-test': 't', 'Wilcox test': 'wilcox'}

ADJUST_P = {'No': 'FALSE', 'Yes': 'TRUE'}

NAME_MAPPING = {'adjustP': 'correct',
                'caseGroup': 'case.group',
                'ce': 'ce',
                'controlGroup': 'control.group',
                'lcType': 'column',
                'pCutoff': 'p.cutoff',
                'polarity': 'polarity',
                'species': 'species',
                'statMethod': 'uni.test',
                'path': 'path'}

a_dic = {'polarity': u'positive', 'control.group': u'g1',
         'column': u'hilic', 'ce': '10', 'species': 'hsa',
         'uni.test': 't', 'p.cutoff': 0.05,
         'path': u'/tmp/metdna-upload\\22cd-7466-4355-ac40\\a75381a1',
         'case.group': u'g2', 'correct': u'No'}

RESULT_FILE_NAME = 'results.tar.gz'

with open('./db_passwd.secret') as f:
    db_pw = f.read().strip()

_ = {'host': 'db', 'user': 'metdna', 'port': 3306,
     'passwd': db_pw, 'db': 'metdna'}  # log in information

Q = {
    'q_pro_queue':  # project queue
        """
        SELECT * FROM `metDNACore_projectqueue` a 
        WHERE a.`status`='waiting' ORDER BY a.`submit_time`;
        """,
    'q_files':  # upload files related to a particular project
        """
        SELECT * FROM `metDNACore_uploadfile` a 
        WHERE a.`project_id`={id:d};
        """,
    'q_user':
        """
        SELECT * FROM `metDNACore_customuser` a WHERE a.`id`={id:d};
        """,
    'q_pro':  # project
        """
        SELECT * FROM `metDNACore_project` a WHERE a.`id`={id:d};
        """,
    'query2':
        """
        SELECT * FROM `metDNACore_projectqueue` a WHERE a.`project_id`=285;
        """,
    'update_before_analysis':  # update 'start_time' in project queue
        """
        UPDATE `metDNACore_projectqueue` SET `status`='{status:s}', `start_time`=NOW() 
        WHERE `project_id`={project_id:d};
        """,
    'update_after_analysis':  # update 'end_time' and 'status' in project queue
        """
        UPDATE `metDNACore_projectqueue` SET `status`='{status:s}', `end_time`=NOW() 
        WHERE `project_id`={project_id:d};
        """
}


BASE_MSG = """\
    <html>
      <head></head>
      <body style="padding: 20px 300px 20px 20px">
        <p>The analysis of your project <b>{project_name:s}</b> has finished!</p>
        <p>please check below url to download your result.</p>
        <p>{url:s}</p>
        <br>
        <div>
        <div style="background-color: #eaf0e2; padding: 5px">
          <p>You received this email because you are using MetDNA at 
          <a href="http://192.168.201.211:8023/index">http://192.168.201.211:8023/index</a>
          </p>
          <br>
          <p>Interdisciplinary Research Center on Biology and Chemistry (IRCBC)</p>
          <p>Shanghai Institute of Organic Chemistry (SIOC)</p>
          <p>Chinese Academy of Sciences (CAS)</p>
          <p>26 Qiuyue Road, Pudong, Shanghai, China 201210</p>
          <p>Website: <a href="www.zhulab.cn">www.zhulab.cn</a></p>
          <div style="height: 50px">
            <img style="height: 50px" src="{metdna_logo:s}">
            &nbsp; &nbsp;
            <img style="height: 50px" src="{zhulab_logo:s}">
          </div>
        </div>
        </div>
      </body>
    </html>
"""


BASE_MSG_ERROR = """\
    <html>
      <head></head>
      <body style="padding: 20px 300px 20px 20px">
        <p>We are very sorry to send you this email because some errors have occurred 
        during the analysis of your project <b>{project_name:s}.</b></p>
        <p>We will check this error later, please wait or send us an email to ask detail directly.</p>
        <br>
        <div>
        <div style="background-color: #eaf0e2; padding: 5px">
          <p>You received this email because you are using MetDNA at 
          <a href="http://192.168.201.211:8023/index">http://192.168.201.211:8023/index</a>
          </p>
          <br>
          <p>Interdisciplinary Research Center on Biology and Chemistry (IRCBC)</p>
          <p>Shanghai Institute of Organic Chemistry (SIOC)</p>
          <p>Chinese Academy of Sciences (CAS)</p>
          <p>26 Qiuyue Road, Pudong, Shanghai, China 201210</p>
          <p>Website: <a href="www.zhulab.cn">www.zhulab.cn</a></p>
          <div style="height: 50px">
            <img style="height: 50px" src="{metdna_logo:s}">
            &nbsp; &nbsp;
            <img style="height: 50px" src="{zhulab_logo:s}">
          </div>
        </div>
        </div>
      </body>
    </html>
"""


def dic2string(para_dic):
    para_str = ''
    for key in para_dic.keys():
        if key not in ['control.group', 'case.group']:
            if key == 'correct' or key == 'p.cutoff':
                para_str += str(key) + '=' + str(para_dic[key]) + ', '
            # elif key == 'p.cutoff':
            #     para_str += str(key) + '='
            else:
                para_str += str(key) + '="' + str(para_dic[key]) + '", '
    groups = (para_dic['control.group'], para_dic['case.group'])
    para_str += 'group=c("{}", "{}")'.format(groups[0], groups[1])
    return para_str


def get_url(root_dir, pol, result_fn="results.tar.gz", log_fn="run.log.txt"):
    """
    Get the urls of result files for website download (web url) and
    the path of log file (local path)
    :param root_dir: MEDIA_ROOT/user_id/project_id (local path), eg: "/tmp/metdna-upload/ffc3-49f4-4559-9979/dd4f85b9"
    :param pol: Positive / Negative / Both
    :param result_fn: result file name, default name is 'results.tar.gz'
    :param log_fn: log file name, default name is 'run.log.txt'
    :return: result url and log path
    """
    pol = pol.lower()
    web_root = root_dir.replace(MEDIA_ROOT, URL)
    result_url_pos = os.path.join(web_root, 'POS', result_fn.replace('results', 'results_pos'))
    result_url_neg = os.path.join(web_root, 'NEG', result_fn.replace('results', 'results_neg'))
    result_url_pathway = os.path.join(web_root, 'POS and NEG', result_fn.replace('results', 'results_pathway'))

    log_path_pos = os.path.join(root_dir, 'POS', log_fn)
    log_path_neg = os.path.join(root_dir, 'NEG', log_fn)
    log_path_both = os.path.join(root_dir, 'POS and NEG', log_fn)
    if pol == 'positive':
        return {'result_url': result_url_pos, 'log_path': log_path_pos}
    elif pol == 'negative':
        return {'result_url': result_url_neg, 'log_path': log_path_neg}
    else:
        return {'result_url': ', '.join([result_url_pos, result_url_neg, result_url_pathway]),
                'log_path': log_path_both}


def check_log_file(url):
    """
    check log file to confirm the result of MetDNA,
    compress all result files if analysis done successfully
    Also check if the result file exist
    :param url: the return of function get_url()
    contains log_path: a string, '.../POS/run.log.txt' for positive mode; './POS and NEG/run.log.txt' for both mode
                         web url: eg: 'http://localhost:8024/media/ffc3-49f4-4559-9979/7bb4839e/POS/results.tar.gz'
    :return: result_status (done: all is well / error: all is error / pos_error / neg_error)
             exist_status (exist: all is well / error: one or both are not exist)
    """
    # pos: 1, neg: 2
    result_status = 'error'
    exist_status = 'exist'
    log_path = url['log_path']
    result_url = url['result_url'].split(', ')  # a list
    print('# result url: ', result_url)
    tar_command_with_log = 'tar -czf {} */ MetDNA.parameters.csv run.log.txt'
    tar_command_no_log = 'tar -czf {} */'
    print('#--------------, in check log file')
    print(tar_command_with_log)
    raw_dir = os.getcwd()
    # deal with url
    result_p_n = []  # local path and file name  [(), ()]
    for url in result_url:
        url = url.replace(URL, MEDIA_ROOT).split('/')
        fn = url.pop()
        result_p_n.append(('/'.join(url), fn))

    if os.path.exists(log_path):
        _ = result_p_n
        with open(log_path) as f:
            log = f.readlines()
            log = [i.strip() for i in log]
        if '##MetDNA is done.' in log:
            result_status = 'done'
            if len(_) == 1:
                _path = _[0]
                cd_des = _path[0]  # cd destination dir
                tar_command = tar_command_with_log.format(_path[1])
                print('# cd command: ', cd_des)
                print('# tar command: ', tar_command)
                os.chdir(cd_des)
                os.system(tar_command)
                print('current dir: ', os.getcwd())
                if os.path.exists(os.path.join(_path[0], _path[1])):
                    shutil.move(_path[1], '../results/{}'.format(_path[1]))
                else:
                    exist_status = 'error'
            elif len(_) == 3:
                for path in _:
                    print('###path is', path, '\n')
                    cd_des = path[0]
                    if 'POS and NEG' in cd_des:
                        tar_command = tar_command_with_log.format(path[1])
                    else:
                        tar_command = tar_command_no_log.format(path[1])
                    print(cd_des, tar_command)
                    os.chdir(cd_des)
                    os.system(tar_command)
                    if os.path.exists(os.path.join(path[0], path[1])):
                        des_path = os.path.join('..', 'results', path[1])
                        if os.path.exists(des_path):
                            os.remove(des_path)
                        shutil.move(path[1], '../results')
                    else:
                        exist_status = 'error'
    os.chdir(raw_dir)
    return {'result_status': result_status, 'exist_status': exist_status}

# para = 'species="hsa", ce="10", polarity="positive", neg.path="D://tmp//metdna-upload//22cd-7466-4355-ac40//7db0829a//NEG", sample.info.pos="sample.info.csv", ' \
#        'pos.path="D://tmp//metdna-upload//22cd-7466-4355-ac40//7db0829a//POS", sample.info.neg="sample.info.csv", uni.test="t", ' \
#        'correct=FALSE, ms1.data.neg="", p.cutoff=0.05, column="hilic", ms1.data.pos="data.csv", group=c("E30", "W15")'
# print(get_url(para, file_name='results.zip'))
# print(dic2string(a_dic))
