import re
import math

def process_out_file(inp_file_name):
    inp_file_path = 'output_files/' + inp_file_name
    final_out_path = 'output_files/' + inp_file_name.replace('.ttl','_final.ttl') 
    with open(inp_file_path) as f:
        lines = f.readlines()
    lines_lst = lines
    pat_id = 0
    mel_id = 0
    addr_plz = 0
    tumor_id = 0
    tnm_id = 0
    op_id = 0
    lbw_id = 0
    op_ops = 0
    OPID = 0

    #to handle PAT_MELDUNGID problem when multiple Meldung_ID exists for same patient
    lst_mel_id = []
    PAT_MELDUNGID_ind = 'F'
    PAT_MELDUNGID_ctr = 0

    #to restrict multiple occurences of '/ADT-GEKID/Agent> .'
    lst_Agent_rep = []

    #to restrict more than 3 consecutive '\n' occurences created due to restriction of multiple '/ADT-GEKID/Agent> .'
    cntr_bp = 0

    for tpl in lines_lst:
        if tpl.count('+') == 2:
           pat_id = tpl.split('+')[1]
        if tpl.count('!') == 2:
           addr_plz = tpl.split('!')[1]
        if tpl.count('*') == 2:
           mel_id = tpl.split('*')[1]
           if not mel_id in lst_mel_id:
              lst_mel_id.append(mel_id)
    
    PAT_ADDR_ID = pat_id + '/1'
    PAT_LABORWERT_ID = pat_id + '/1'
    rep_pat_id = '+'+str(pat_id)+'+'
    rep_addr_plz = '!'+str(addr_plz)+'!'
    new_ttl_list = []
    lst_redundant_tpl = []
    
    for tpl in lines_lst:
        if tpl.count('*') == 2:
           mel_id = tpl.split('*')[1]
           if not mel_id in lst_mel_id:
              lst_mel_id.append(mel_id)
        #print('Formatting output file for Patient Id {} having Meldung Id {} \n \n'.format(pat_id,mel_id))

        if tpl.count('~') == 2:
           tumor_id = tpl.split('~')[1]
        #start of formatting for Laborwert
        if tpl.count("'") == 2:
           lbw_id = tpl.split("'")[1]

        if tpl.count('°') == 2:
           tnm_id = tpl.split('°')[1]

        PAT_MELDUNGID = str(mel_id)
        PAT_MELDUNG_ID = str(mel_id) + '/' + str(tumor_id)
        rep_mel_id = '*'+str(mel_id)+'*'
        TUMOR_ID_TNM = str(tumor_id) + '/' + str(tnm_id)

        rep_tumor_id = '~'+str(tumor_id)+'~'
        rep_tnm_id = '°'+str(tnm_id)+'°'

        if tpl.count("'") == 2:
           lbw_id = tpl.split("'")[1]

        rep_lbw_id = "'"+str(lbw_id)+"'"
        if rep_lbw_id in tpl:
           tpl = tpl.replace(rep_lbw_id,PAT_LABORWERT_ID)
        if 'PAT_LABORWERT_ID' in tpl:
           tpl = tpl.replace('PAT_LABORWERT_ID',PAT_LABORWERT_ID)
        
        #start of formatting for OP_ID
        if tpl.count("=") == 2:
           op_id = tpl.split("=")[1]
           #OPID = str(op_id)

        if 'OPID' in tpl:
           OPID += 1
           tpl=tpl.replace('OPID',str(math.ceil(OPID/3)))

        #start of formatting for OP_OPS
        OP_ID_OPS = str(op_id) + '/1'
        if 'OP_ID_OPS' in tpl:
           tpl = tpl.replace('OP_ID_OPS',OP_ID_OPS)

        if tpl.count("´") == 2:
           op_ops = tpl.split("´")[1]
        rep_op_ops = "´"+str(op_ops)+"´"
        if rep_op_ops in tpl:
           tpl = tpl.replace(rep_op_ops,'1')

        rep_op_id = "="+str(op_id)+"="
        if rep_op_id in tpl:
           tpl = tpl.replace('=','')
        #end of formatting for OP_ID


        #start of formatting for Patient_ID
        if rep_pat_id in tpl:
           tpl = tpl.replace(rep_pat_id,pat_id)

        if 'PAT_ID' in tpl:
           tpl = tpl.replace('PAT_ID',pat_id)

        #start of formatting for Patient Adress
        if rep_addr_plz in tpl:
           tpl = tpl.replace(rep_addr_plz,PAT_ADDR_ID)

        if 'PAT_ADDR_ID' in tpl:
           tpl = tpl.replace('PAT_ADDR_ID',PAT_ADDR_ID)

        #start of formatting for Meldung id
        if rep_mel_id in tpl:
           tpl = tpl.replace(rep_mel_id,mel_id)

        print('PAT_MELDUNGID_ctr :',PAT_MELDUNGID_ctr)
        print('length of lst_mel_id: ',len(lst_mel_id))
        #print('length of lst_mel_id is: ',len(lst_mel_id))
        if 'Tumorzuordnung/PAT_MELDUNGID' in tpl and len(lst_mel_id)>0:
           tpl = tpl.replace('Tumorzuordnung/PAT_MELDUNGID','Tumorzuordnung/'+lst_mel_id[PAT_MELDUNGID_ctr])
           print('PAT_MELDUNGID replaced by',lst_mel_id[PAT_MELDUNGID_ctr])
           PAT_MELDUNGID_ind = 'T'
        if PAT_MELDUNGID_ind == 'T' and tpl=='\n' and PAT_MELDUNGID_ctr<len(lst_mel_id):
           PAT_MELDUNGID_ctr += 1
           PAT_MELDUNGID_ind = 'F'


        if 'PAT_MELDUNGID' in tpl:
           tpl = tpl.replace('PAT_MELDUNGID',PAT_MELDUNGID)

        if 'PAT_MELDUNG_ID' in tpl:
           tpl = tpl.replace('PAT_MELDUNG_ID',PAT_MELDUNG_ID)

        #start of formatting for tumor id
        if rep_tumor_id in tpl:
           tpl = tpl.replace(rep_tumor_id,tumor_id)   
        if 'TUMORID' in tpl:
           tpl = tpl.replace('TUMORID',str(tumor_id))

        #start of formatting for tnm id
        if rep_tnm_id in tpl:
           tpl = tpl.replace(rep_tnm_id,tnm_id)
        if 'TUMOR_ID_TNM' in tpl:
           tpl = tpl.replace('TUMOR_ID_TNM',TUMOR_ID_TNM)

        #to restrict multiple occurences of '/ADT-GEKID/Agent> .'
        allow_tpl = True
        if '/ADT-GEKID/Agent> .' in tpl:
           if not tpl in lst_Agent_rep:
              lst_Agent_rep.append(tpl)
              allow_tpl = True
           else:
              allow_tpl = False

        ##to restrict more than 5 consecutive '\n'
        #allow_bp_in_tpl = True
        #if '\n' in tpl:
        #   cntr_bp += 1
        #   if cntr_bp > 5:
        #      allow_bp_in_tpl = False
        #   else:
        #      allow_bp_in_tpl = True
        #else:
        #   cntr_bp = 0

        if allow_tpl:       
           new_ttl_list.append(tpl)
    #new_ttl_list.reverse()

    #to remove repetitions, mainly of '\n'
    # e.g from [1,1,1,1,1,1,2,3,4,4,5,1,2] to [1, 2, 3, 4, 5, 1, 2]
    from itertools import groupby
    formated_ttl_list = [x[0] for x in groupby(new_ttl_list)]
    print('length of list is: ',len(formated_ttl_list))    

    f=open(final_out_path,'w')
    f.writelines(formated_ttl_list)
    f.close()
    return formated_ttl_list
