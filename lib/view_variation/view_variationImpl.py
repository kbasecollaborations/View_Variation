# -*- coding: utf-8 -*-
#BEGIN_HEADER
import logging
import os
import uuid

from installed_clients.KBaseReportClient import KBaseReport
from view_variation.Utils.htmlreportutils import htmlreportutils
from view_variation.Utils.variationutils import variationutils
#END_HEADER


class view_variation:
    '''
    Module Name:
    view_variation

    Module Description:
    A KBase module: view_variation
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/man4ish/view_variation.git"
    GIT_COMMIT_HASH = "a1e00e3b90653953193d1adc953f6e80015fcc2a"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.INFO)
        self.hr = htmlreportutils()
        self.vu = variationutils()
        #END_CONSTRUCTOR
        pass


    def run_view_variation(self, ctx, params):
        """
        This example function accepts any number of parameters and returns results in a KBaseReport
        :param params: instance of type "InputParams" -> structure: parameter
           "vcf_ref" of String, parameter "workspace_name" of String,
           parameter "genome_or_assembly_ref" of String
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_view_variation
        workspace = params['workspace_name']
        outputdir = self.shared_folder + '/' + str(uuid.uuid1())
        os.mkdir(outputdir)
        

        '''
        report_info = report.create({'report': {'objects_created':[],
                                                'text_message': params['parameter_1']},
                                                'workspace_name': params['workspace_name']})
        '''                                        
        output = self.hr.create_html_report(self.callback_url, outputdir, workspace)
        self.vu.prepare_genome(outputdir, "genome_file")
        self.vu.prepare_vcf(outputdir, "vcf_fie")
        report = KBaseReport(self.callback_url)
        #END run_view_variation

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_view_variation return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
