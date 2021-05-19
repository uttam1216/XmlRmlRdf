import argparse
import os
from os import listdir
from os.path import isfile, join
from rmlm_format_intermediate_out import *
import time

class transform:
      def __init__(self,home_path):
          #format of command to be run inside rmlmapper folder for processing the rules file to convert an input xml to output rml
          self.st1 = "java -jar target/rmlmapper-4.9.4-r351-all.jar --mappingfile "+home_path+"rmlm_intermediate_rule_files/"
          self.st2 = " --outputfile "+home_path+"rmlm_output_files/"
          self.st3 = " -d"
          self.home_path = home_path
          print(home_path)

      def run_rules(self):
          #opening RML rules file
          with open(self.home_path+'rmlm_rules.rml.ttl') as f:
               lines = f.readlines()
          #a global list to store all output lines 
          global_out_list = []

          #names of the list of xml files that needs to be converted to rml
          lst_input_files = [f for f in listdir(self.home_path+'rmlm_input_files/') if isfile(join(self.home_path+'rmlm_input_files/', f))]

          #for each of these files, 
          for item in lst_input_files:
              lst_rml_contents = [w.replace('replaceable_patient_file_name', 'rmlm_input_files/'+item) for w in lines]
              lst_rml_contents.append('\n')
              #save this list of contents to a file which needs to be executed   
              f_out=open(self.home_path+'rmlm_intermediate_rule_files/'+item.replace('.xml','')+'_rules.rml.ttl','w')
              f_out.writelines(lst_rml_contents)
              f_out.close()

   
          lst_intermediate_files = [f for f in listdir(self.home_path+'rmlm_intermediate_rule_files/') if isfile(join(self.home_path+'rmlm_intermediate_rule_files/', f))]
          for item in lst_intermediate_files:
              st = self.st1 + item + self.st2 + item.replace('_rules.rml.ttl','_out.ttl') + self.st3
              os.system(st)
              new_ttl_list = process_out_file(item.replace('_rules.rml.ttl','_out.ttl'))
              new_ttl_list.append('\n \n \n \n \n')
              global_out_list += new_ttl_list

          #writing out the one final combined output file
          f_out=open(self.home_path+'rmlm_final_combined_output.rml.ttl','w')
          f_out.writelines(global_out_list)
          f_out.close()

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='Path of med2icin folder')
   parser.add_argument('--path', type=str)
   input_args = parser.parse_args()
   if input_args.path is None:
      home_path =  "/home/ukumar/Desktop/med2icin/"
   else:
      home_path = input_args.path
   st = time.time()
   obj_transform = transform(home_path)
   obj_transform.run_rules()
   et = time.time()
   print('Total time taken: ',str(et-st))

