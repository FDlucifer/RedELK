#!/usr/bin/python3
"""
Part of RedELK

This alarm always triggers. It lists the last 2 redirtraffic lines as hit

Authors:
- Outflank B.V. / Mark Bergman (@xychix)
- Lorenzo Bernardi (@fastlorenzo)
"""
import logging
import traceback

from modules.helpers import get_hits_count, get_initial_alarm_result, get_query

info = {
    'version': 0.1,
    'name': 'lastline alarm module',
    'alarmmsg': 'ALARM GENERATED BY LASTLINE',
    'description': 'This alarm always triggers. It lists the last 2 redirtraffic lines as hit',
    'type': 'redelk_alarm-NOTINUSE',
    'submodule': 'alarm_lastline'
}


class Module():
    """ lastline alarm module """
    def __init__(self):
        self.logger = logging.getLogger(info['submodule'])

    def run(self):
        """ Run the alarm module """
        ret = get_initial_alarm_result()
        ret['info'] = info
        ret['fields'] = ['source.ip', 'source.nat.ip', 'source.geo.country_name', 'source.as.organization.name', 'redir.frontend.name', 'redir.backend.name', 'infra.attack_scenario', 'tags', 'redir.timestamp']
        ret['groupby'] = ['source.ip']
        try:
            report = self.alarm_check()
            ret['hits']['hits'] = report['hits']
            ret['hits']['total'] = len(report['hits'])
        # pylint: disable=broad-except
        except Exception as error:
            stack_trace = traceback.format_exc()
            ret['error'] = stack_trace
            self.logger.exception(error)
        self.logger.info('finished running module. result: %s hits', ret['hits']['total'])
        return ret

    # pylint: disable=no-self-use
    def alarm_check(self):
        """ This check queries for IP's that aren't listed in any iplist* but do talk to c2* paths on redirectors """
        es_query = "*"
        i = get_hits_count(es_query)
        i = min(i, 10000)
        es_result = get_query(es_query, i)
        report = {}
        report['hits'] = []
        report['hits'].append(es_result[0])
        report['hits'].append(es_result[1])
        return report
