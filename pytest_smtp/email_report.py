#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : email_report.py
@Time  : 2021/3/31 15:35
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import sys
import time
import socket
import platform

from pytest_html.plugin import HTMLReport
from email_template import EMAIL_REPORT_TEMPLATE


__author__ = "tao.xu"
__version__ = "1.5.1"
POSIX = os.name == "posix"
WINDOWS = os.name == "nt"
STATUS = {
    0: 'PASS',
    1: 'FAIL',
    2: 'ERROR',
    3: 'SKIP',
    4: 'PASS(Canceled By User)',
}


def get_local_ip():
    """
    Get the local ip address --linux/windows
    :return:(char) local_ip
    """
    return socket.gethostbyname(socket.gethostname())


def get_local_hostname():
    """
    Get the local ip address --linux/windows
    :return:
    """
    return socket.gethostname()


class EmailReport(HTMLReport):
    local_hostname = get_local_hostname()
    local_ip = get_local_ip()

    def __init__(self, logfile, config, *args, **kwargs):
        super(EmailReport, self).__init__(logfile, config)
        self.tester = config.getoption('--tester') or config.getini('tester') or __author__
        self.test_desc = config.getoption('--desc') or config.getini('desc') or ""
        self.test_version = "TODO"
        self.test_env = {}
        self.test_nodes = None
        self.report_title = None
        self.report_html = "./report.html"

    @property
    def pass_ratio(self):
        result = 0
        try:
            result = self.passed / (self.failed + self.passed)
        except ZeroDivisionError:
            pass
        return result

    @property
    def num_tests(self):
        return self.passed + self.failed + self.xpassed + self.xfailed

    def _get_attributes(self):
        """
        Return report attributes as a list of (name, value).
        Override this to add custom attributes.
        :param result:
        :return:
        """

        suite_stop_time = time.time()
        suite_time_delta = suite_stop_time - self.suite_start_time

        attr = {
            'Tester': self.tester,
            'Version': self.test_version,
            'Start': str(self.suite_start_time),
            'End': str(suite_stop_time),
            'Elapsed': suite_time_delta,
            'Location': '{0}({1})'.format(self.local_hostname, self.local_ip),
            'Workspace': os.getcwd(),
            'Command': 'python ' + ' '.join(sys.argv),
            'Python': platform.python_version(),
        }
        if self.test_desc:
            attr = dict(attr, **({'Description': self.test_desc}))

        return dict(attr, **self.test_env)

    def _get_attributes_table_string(self):
        """
        get attributes table_string
        """
        att_template = """
        <tr id='attr_%d' class='attr'>
            <td colspan='1' align='left' width='15%%'>%s</td>
            <td colspan='1' align='left'>%s</td>
        </tr>
        """
        tr = ""
        attr = self._get_attributes()
        for idx, (k, v) in enumerate(attr.items()):
            idx += 1
            if v:
                tr += att_template % (idx, k, v)
        return tr

    def _get_nodes_table_string(self, nodes_info=None):
        """
        nodes_info [
            {
                Name:''
                Status:''
                IPAddress:''
                Roles:''
                User:''
                Password:''
            }
        ]
        """
        if nodes_info is None:
            nodes_info = []
        nodes_info.insert(0, {
            "Name": self.local_hostname,
            "Status": "Ready",
            "IPAddress": self.local_ip,
            "Roles": "Executor",
            "User": "root",
            "Password": "********",
            "OS": platform.system(),
        })
        html_template = """
        <tr id='node_%d' class='nodes'>
            <td colspan='1' align='center'>%s</td>
            <td colspan='1' align='center'>%s</td>
            <td colspan='1' align='center'>%s</td>
            <td colspan='1' align='center'>%s</td>
            <td colspan='1' align='center'>%s</td>
            <td colspan='1' align='center'>%s</td>
            <td colspan='1' align='center'>%s</td>
        </tr>
        """
        tr = ""
        for idx, node in enumerate(nodes_info):
            tr += html_template % (idx, node["Name"], node["Status"], node["IPAddress"],
                                   node["Roles"], node["User"], node["Password"], node["OS"])
        return tr

    def _get_result_table_string(self):
        html_template = """
        <tr id='result_%d' class='%s'>
            <td colspan='1' align='left'>%s</td>
            <td colspan='1' align='center'>%s</td>
            <td colspan='1' align='center'>%s</td>
            <td colspan='1' align='center'>%d</td>
        </tr>
        """

        msg_template = """
        <tr id='msg_%d' class='%s'>
            <td colspan='1' align='left'>Message</td>
            <td colspan='3' align='left'><pre>%s</pre></td>
        </tr>
        """

        tr = ""
        for idx, result in enumerate(self.results):
            name = result.test_id
            doc = ""
            desc = doc and ('%s: %s' % (name, doc)) or name
            output = result.row_extra
            n = 0
            if n == 0:
                style = 'passCase'
            elif n == 1:
                style = 'failCase'
            elif n == 2:
                style = 'errorCase'
            elif n == 3:
                style = 'skipCase'
            elif n == 4:
                style = 'passCase'
            else:
                style = 'none'
            tr += html_template % (idx, style, desc, STATUS[n], result.time, 1)
            if output:
                tr += msg_template % (idx, style, output)
        return tr

    def generate_report_body(self):
        self.report_title = "PASS" + ": " + self.report_title
        attr = self._get_attributes_table_string()
        results = self._get_result_table_string()
        nodes = self._get_nodes_table_string(self.test_nodes)
        title_color = "h_red" if STATUS[1] in self.report_title or STATUS[2] in self.report_title else "h_green"
        body = EMAIL_REPORT_TEMPLATE % dict(
            Title=self.report_title,
            TitleColor=title_color,
            Generator=__author__,
            Environment=attr,
            Nodes=nodes,
            Total=str(self.num_tests),
            Pass=str(self.passed),
            Fail=str(self.failed),
            Error=str(self.errors),
            Skip=str(self.skipped),
            Cancel=str(0),
            Passrate="{0:.2%}".format(self.pass_ratio),
            Results=results
        )

        report_path_dir = os.path.dirname(self.report_html)
        if not os.path.isdir(report_path_dir):
            try:
                os.makedirs(report_path_dir)
            except OSError as e:
                raise Exception(e)
        with open(self.report_html, 'wb') as f:
            f.write(body.encode('UTF-8'))

        return body


if __name__ == '__main__':
    pass
