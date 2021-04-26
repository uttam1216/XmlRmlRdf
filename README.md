#Pre-requisite:
 #Maven
 #jdk
 #RML Mapper (https://github.com/RMLio/rmlmapper-java) and build using mvn install to generate 2 .jar files.
 #Name of the jar files generated should match that already written in python script rmlm_transform_inp_xml_to_rml.py

#Keep all files as present in above repository in a folder with same name i.e. "med2icin" 
#Open a terminal and get inside the rmlmapper folder and then run command equivalent to following as per your folders:

ukumar@eis-london:~/rmlmapper-java-master$ python /home/ukumar/Desktop/med2icin/rmlm_transform_inp_xml_to_rml.py --path /home/ukumar/Desktop/med2icin/

#where, path is a parameter being passed, supposed to be the path of med2icin folder
#all necessary files will run in auto. Basically, running above command, takes all input files from the 'input_files' folder inside med2icin
#and then creates RML rules for each of them and keeps them in an intermediate folder(rmlm_intermediate_rule_files) and then runs them for output. 
#The output once generated(in folder rmlm_output_files), are formated in auto by call of a function in format_intermediate_out.py script called by itself.
#final output are files inside folder rmlm_output_files with extension as "<input_file_name>_out_final.ttl"
