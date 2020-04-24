import os
import json
import subprocess
import shutil
import requests

class variationutils:
    def __init__(self):
        self.organism_dict = {}
        self.url = "https://appdev.kbase.us/dynserv/f1b4482974ac4ea5a7187aef173d5cfd91a66907.VariationFileServ/create_cache"  #hardcoded for testing
        self.service_token = "JJPRPDD7XZWC54Q7WE2HKM3AWZDKZL3F"  #hardcoded for testing
        self.variation_ref = "39465/42/22"
        pass

    def make_request(self, variation_ref, service_token, url):
        """"Helper to make a JSON RPC request with the given workspace ref."""
        post_data = {
            "variation_ref": variation_ref,
            "auth_token": service_token
        }
        headers = {'Content-Type': 'application/json', 'Authorization': service_token}
        resp = requests.post(url, data=json.dumps(post_data), headers=headers)
        return (resp.text)

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
        genome_file = "*.fa_assembly.fa"
        cmd = "/jbrowse/bin/prepare-refseqs.pl --fasta " + "/kb/module/work/tmp/"+ genome_file +" --out " + output_dir + "/jbrowse/data"
        #self.run_cmd(cmd)

    def prepare_vcf(self, output_dir, vcf_file):
        '''
        function for preparing vcf file
        '''
        vcf_file = "original_snps.vcf"
        #shutil.copy("/kb/module/work/tmp/corona_vcf/"+ vcf_file, output_dir + "/jbrowse/data")
        os.system("cp /kb/module/work/tmp/*_vcf/"+ vcf_file + output_dir + "/jbrowse/data")
        zipcmd = "bgzip "  + output_dir + "/jbrowse/data/original_snps.vcf"
        self.run_cmd(zipcmd)
        indexcmd = "tabix -p vcf " + output_dir + "/jbrowse/data/"+ vcf_file
        self.run_cmd(indexcmd)

    def updateJson(self, output_dir, trackname, gz_filename, tbi_filename):
        '''
        function for updating json file with track information
        '''
        resp = self.make_request(self.variation_ref, self.service_token, self.url)
        data = json.loads(resp)
        new_dict = dict()
        for j in data:
            url = data[j]
            newurl = url.replace("http://appdev.kbase.us",
                                 "https://appdev.kbase.us/dynserv/f1b4482974ac4ea5a7187aef173d5cfd91a66907.VariationFileServ/")
            new_dict[j] = newurl


        vcf_gz_filename = new_dict.get("vcf")
        vcf_tbi_filename = new_dict.get("vcf_index")
        ref_filename = new_dict.get("assembly")
        index_ref_filename = new_dict.get("assembly_index")

        jsonfile = output_dir + "/jbrowse/data/trackList.json"

        data = {}
        with open(jsonfile) as json_file:
           data = json.load(json_file)
           data['tracks'].append({
           'label': trackname,
           'key': trackname,
           'storeClass': 'JBrowse/Store/SeqFeature/VCFTabix',
           'urlTemplate'    : vcf_gz_filename,
           'tbiUrlTemplate' : vcf_tbi_filename,
           'type'          : 'JBrowse/View/Track/HTMLVariants'
           })
        data['tracks'][0]['urlTemplate'] = ref_filename
        data['tracks'][0]['faiUrlTemplate'] = index_ref_filename
        data['tracks'][0]['storeClass'] = 'JBrowse/Store/SeqFeature/IndexedFasta'
        with open(jsonfile, 'w') as outfile:
           json.dump(data, outfile) 
