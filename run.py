# -*- coding: utf-8 -*-


import os, sys
import logging

logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setupJmx(jmx_prefix, threads_num, rampup_time, duration, remark, setHost=False):
    current_dir = os.getcwd()
    template_jmx = os.path.join(current_dir, 'template', jmx_prefix + '.jmx')
    if not os.path.exists(template_jmx):
        logger.error(template_jmx + ' path not Exist')
        return None

    new_jmx_dir = "{}_tn{}_rt{}_d{}_r{}".format(jmx_prefix, threads_num, rampup_time, duration, remark)
    new_jmx_path = new_jmx_dir + '.jmx'
    logger.info("jmx name: " + new_jmx_path)

    result_dir = os.path.join(current_dir, new_jmx_dir, 'result')
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    with open(template_jmx) as temp_stream:
        lines = temp_stream.readlines()
        with open(os.path.join(current_dir, new_jmx_path), 'w') as new_stream:
            for line in lines:
                new_line = line.replace('$threads_num$', threads_num)
                if setHost:
                    new_line = new_line.replace('<stringProp name="HTTPSampler.domain">www.baidu.com</stringProp>', '<stringProp name="HTTPSampler.domain">${__P(url,)}</stringProp>')
                new_stream.write(new_line)
                
    return new_jmx_dir

def runJmeterByCmd(new_jmx_dir, hostname='', ip=''):
    def isJmeterInstalled():
        result = True
        lines = os.popen('which jmeter')
        for l in lines:
            if 'not found' in l:
                logger.error('Jmeter Not Installed')
                result = False
                break
        return result
    if hostname:
        execute_cmd = 'jmeter -Jurl={1} -n -t {0}.jmx -l {0}.jtl -j {0}.log -f -e -o {0}/result/'.format(new_jmx_dir, hostname)
    else:    
        execute_cmd = 'jmeter -n -t {0}.jmx -l {0}.jtl -j {0}.log -f -e -o {0}/result/'.format(new_jmx_dir)
    logger.info(execute_cmd)
    if isJmeterInstalled():
        os.system(execute_cmd)


if __name__ == '__main__':
    if len(sys.argv[1:]) == 5:
        logger.info('param list: ', str(sys.argv[1:]))
        param = sys.argv[1:]
        new_jmx_dir = setupJmx(param[0], param[1], param[2], param[3], param[4], True)
        if new_jmx_dir and param:
            runJmeterByCmd(new_jmx_dir, 'www.zhihu.com')



