import os
from os import listdir
from os.path import isfile, join
from format_intermediate_out import *

#format of command to be run on flink for processing the rules file for converting an input xml to output rml
st1 = "../../flink-1.12.0/bin/flink run /home/ukumar/RMLStreamer/target/RMLStreamer-2.0.1-SNAPSHOT.jar toFile --mapping-file /home/ukumar/Desktop/med2icin/intermediate_rule_files/"
st2 = " --output-path /home/ukumar/Desktop/med2icin/output_files/"
st3 = "_out.ttl"

#opening RML rules file
with open('rules.rml.ttl') as f:
     lines = f.readlines()
#a global list to store all output lines
global_out_list = []

#names of the list of xml files that needs to be converted to rml
lst_input_files = [f for f in listdir('input_files/') if isfile(join('input_files/', f))]

#for each of these files, 
for item in lst_input_files:
    lst_rml_contents = [w.replace('replaceable_patient_file_name', 'input_files/'+item) for w in lines]
    lst_rml_contents.append('\n')
    #save this list of contents to a file which needs to be executed   
    f_out=open('intermediate_rule_files/'+item.replace('.xml','')+'_rules.rml.ttl','w')
    f_out.writelines(lst_rml_contents)
    f_out.close()

   
lst_intermediate_files = [f for f in listdir('intermediate_rule_files/') if isfile(join('intermediate_rule_files/', f))]
for item in lst_intermediate_files:
    st = st1 + item + st2 + item.replace('_rules.rml.ttl','') + st3
    os.system(st)
    new_ttl_list = process_out_file(item.replace('_rules.rml.ttl','')+'_out.ttl')
    new_ttl_list.append('\n \n \n \n \n')
    global_out_list += new_ttl_list

#writing out the one final combined output file
f_out=open('final_combined_output.rml.ttl','w')
f_out.writelines(global_out_list)
f_out.close()

