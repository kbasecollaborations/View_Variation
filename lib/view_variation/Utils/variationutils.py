import uuid
import os
import json
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.WorkspaceClient import Workspace
import shutil 

class variationutils:
    def __init__(self):
        self.organism_dict = {}
        pass

    def prepare_genome(self, output_dir, genome_file):
        '''
        function for preparing genome
        '''
        os.system("perl -MCPAN -Mlocal::lib=my_lwp -e 'CPAN::install(LWP)'")
        os.system("perl -MCPAN -Mlocal::lib=--self-contained,my_lwp -e 'CPAN::install(LWP)'")
        os.system(output_dir+"/jbrowse/setup.sh")
        cmd = output_dir + "/jbrowse/bin/prepare-refseqs.pl --fasta " + "/kb/module/test/sample_data/GCA_009858895.3_ASM985889v3_genomic.gbff_genome_assembly.fa_assembly.fa"
        os.system(cmd)

    def prepare_vcf(self, output_dir, vcf_file):
        '''
        function for preparing vcf file
        '''
        os.system("cp /kb/module/test/sample_data/snps.vcf " + output_dir)
        zipcmd = "bgzip "  + output_dir + "/snps.vcf"
        os.system(zipcmd)
        indexcmd = "tabix -p vcf " + output_dir + "/snps.vcf.gz"
        os.system(indexcmd)

    def updateJson(jsonfile, trackname):
        '''
        function for updating json file with track information
        '''
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
