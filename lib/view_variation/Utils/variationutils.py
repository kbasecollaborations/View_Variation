import uuid
import os
import json
import subprocess
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.WorkspaceClient import Workspace

import shutil 

class variationutils:
    def __init__(self):
        self.organism_dict = {}
        pass

    def run_cmd(self, cmd):
        try:
           process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
           stdout, stderr = process.communicate()
           if stdout:
               print ("ret> ", process.returncode)
               print ("OK> output ", stdout)
           if stderr:
               print ("ret> ", process.returncode)
               print ("Error> error ", stderr.strip())

        except OSError as e:
           print ("OSError > ", e.errno)
           print ("OSError > ", e.strerror)
           print ("OSError > ", e.filename)

    def prepare_genome(self, output_dir, genome_file):
        '''
        function for preparing genome
        '''
        cmd = "/jbrowse/bin/prepare-refseqs.pl --fasta " + "/kb/module/work/tmp/*.fa_assembly.fa --out " + output_dir + "/jbrowse/data"
        self.run_cmd(cmd)
        #cmd = "/jbrowse/bin/prepare-refseqs.pl --fasta " + "/kb/module/test/sample_data/GCA_009858895.3_ASM985889v3_genomic.gbff_genome_assembly.fa_assembly.fa --out " + output_dir + "/jbrowse/data"
        #os.system(cmd)

    def prepare_vcf(self, output_dir, vcf_file):
        '''
        function for preparing vcf file
        '''
        #os.system("cp /kb/module/test/sample_data/snps.vcf " + output_dir + "/jbrowse/data")
        os.system("cp /kb/module/work/tmp/*_vcf/original_snps.vcf " + output_dir + "/jbrowse/data")
        zipcmd = "bgzip "  + output_dir + "/jbrowse/data/original_snps.vcf"
        self.run_cmd(zipcmd)
        #os.system(zipcmd)
        indexcmd = "tabix -p vcf " + output_dir + "/jbrowse/data/original_snps.vcf.gz"
        self.run_cmd(indexcmd)
        #os.system(indexcmd)

    def updateJson(self, output_dir, trackname):
        '''
        function for updating json file with track information
        '''
        jsonfile = output_dir + "/jbrowse/data/trackList.json"
        data = {}
        with open(jsonfile) as json_file:
           data = json.load(json_file)
           data['tracks'].append({
           'label': trackname,
           'key': trackname,
           'storeClass': 'JBrowse/Store/SeqFeature/VCFTabix',
           'urlTemplate'   : trackname,
           'type'          : 'JBrowse/View/Track/HTMLVariants'
           })
       
        with open(jsonfile, 'w') as outfile:
           json.dump(data, outfile) 
