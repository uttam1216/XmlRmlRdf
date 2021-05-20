import re
import math

def process_out_file(inp_file_name):
    inp_file_path = '/home/ukumar/Desktop/med2icin/rmlm_output_files/' + inp_file_name
    final_out_path = '/home/ukumar/Desktop/med2icin/rmlm_output_files/' + inp_file_name.replace('.ttl','_final.ttl') 
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
    melder_id = 0
    absender_id = 0
    #Menge_Fruehere_Tumorerkrankung ID
    mft_id = 0
    #Diagnose Menge Hist ID
    menge_hist_id = 0
    #Diagnose Module_Mama_ID
    mod_mama_id = 0

    #to handle PAT_MELDUNGID problem when multiple Meldung_ID exists for same patient
    lst_mel_id = []
    PAT_MELDUNGID_ind = 'F'
    PAT_MELDUNGID_ctr = 0
    PAT_MELDUNGID_D_ind = 'F'
    PAT_MELDUNGID_O_ind = 'F'
    PAT_MELDUNGID_D_ctr = 0
    PAT_MELDUNGID_O_ctr = 0
    #MELID_ind = 'F'
    #MELID_ctr = 0

    #list of collection of distinct laborwert_typ to use be replaced by incemental counter as id does not exist for laborwert
    distinct_laborwert_lst = []
    #default index of laborwert_typ replacement since id does not exist for laborwert
    idx_of_lab_typ = 0

    #to handle PAT_MELDUNGID of OPReport
    lst_opr_mel_id = []

    #to restrict multiple occurences of '/ADT-GEKID/Agent> .'
    lst_Agent_rep = []

    #to restrict more than 3 consecutive '\n' occurences created due to restriction of multiple '/ADT-GEKID/Agent> .'
    cntr_bp = 0

    #clinical TNM Finding
    cTNM_id = 0

    #pathological TNM Finding
    pTNM_id = 0

    #parsing the intermediate file so as to format it using the ids fetched in this loop
    for tpl in lines_lst:
        try:
           #fetching Patient ID
           if tpl.count('+') == 2:
              pat_id = tpl.split('+')[1]
           #fetching Melder ID
           if tpl.count('µ') == 2:
              melder_id = tpl.split('µ')[1]
           #fetching Absender ID
           if tpl.count('α') == 2:
              absender_id = tpl.split('α')[1]
           #fetching Menge Histologie ID
           if tpl.count('γ') == 2:
              menge_hist_id = tpl.split('γ')[1]

           #fetching one of the address field to make it ID
           if tpl.count('!') == 2:
              addr_plz = tpl.split('!')[1]
           #fetching Meldung ID
           if tpl.count('*') == 2:
              mel_id = tpl.split('*')[1]
              if not mel_id in lst_mel_id:
                 lst_mel_id.append(mel_id)
           #fetching Tumor ID
           if tpl.count('~') == 2:
              tumor_id = tpl.split('~')[1]
           #fetching one of the Laborwert field to make it ID 
              if tpl.count("'") == 2:
                 lbw_id = tpl.split("'")[1]
                 if not str(lbw_id) in distinct_laborwert_lst:
                    distinct_laborwert_lst.append(str(lbw_id))
           #start of formatting for cTNM
           if tpl.count("°") == 2:
              cTNM_id = tpl.split("°")[1]

           #start of formatting for pTNM
           if tpl.count("ρ") == 2:
              pTNM_id = tpl.split("ρ")[1]
        except Exception as ex:
           print('Got exception while fetching one of the ids for formatting.')
           print(ex)

    '''
    for tpl in reversed(lines_lst): 
        if tpl.count('*') == 2:
           mel_id = tpl.split('*')[1]
        #forming a list of meldung id in which OPReport exists
        if 'OPReport/O_PAT_MELDUNGID' in tpl:
           if mel_id != 0 and not mel_id in lst_opr_mel_id:
              lst_opr_mel_id.append(mel_id)
    print('lst_opr_mel_id is: ',lst_opr_mel_id)
    '''
    #print('list of laborwert_typ is',distinct_laborwert_lst)

    new_ttl_list = []
    lst_redundant_tpl = []
    rep_ft_ZZ = ''
    rep_ft_YY = ''
    rep_ft_XX = ''
    rep_ft_WW = ''
    rep_ft_VV = ''
    rep_ft_UU = ''
    rep_ft_TT = ''
    rep_ft_SS = ''
    rep_ft_RR = ''
    rep_ft_QQ = ''
    PAT_ADDR_ID = str(pat_id) + '/1'
    PAT_LABORWERT_ID = str(pat_id) + '/1'
    rep_pat_id = '+'+str(pat_id)+'+'
    rep_melder_id = 'µ'+str(melder_id)+'µ'
    rep_addr_plz = '!'+str(addr_plz)+'!'
    rep_absender_id = 'α'+str(absender_id)+'α'
    rep_menge_hist_id = 'γ'+str(menge_hist_id)+'γ'

    
    for tpl in lines_lst:
        
        '''
        #start of formatting for Fruehere_Tumorerkrankung
        if tpl.count('Z') == 2 and '/Fruehere_Tumorerkrankung/' in tpl:
           ft_ZZ = tpl.split('Z')[1]
           rep_ft_ZZ = 'Z'+str(ft_ZZ)+'Z'    

        if rep_ft_ZZ in tpl and '/Fruehere_Tumorerkrankung/' in tpl:
           tpl = tpl.replace(rep_ft_ZZ,'1')
        #end of formatting for Fruehere_Tumorerkrankung


        #start of formatting for Modul_Mamma
        if tpl.count('Y') == 2 and '/Modul_Mamma/' in tpl:
           ft_YY = tpl.split('Y')[1]
           rep_ft_YY = 'Y'+str(ft_YY)+'Y'    

        if rep_ft_YY in tpl and '/Modul_Mamma/' in tpl:
           tpl = tpl.replace(rep_ft_YY,'1')       
        #end of formatting for Modul_Mamma

        #start of OPResidualTumorStatus
        if tpl.count('X') == 2 and '/Residualstatus/' in tpl:
           ft_XX = tpl.split('X')[1]
           rep_ft_XX = 'X'+str(ft_XX)+'X'    

        if rep_ft_XX in tpl and '/Residualstatus/' in tpl:
           tpl = tpl.replace(rep_ft_XX,'1')        
        #end of OPResidualTumorStatus

        #start of Menge_Komplikation
        if tpl.count('W') == 2 and '/Menge_Komplikation/' in tpl:
           ft_WW = tpl.split('W')[1]
           rep_ft_WW = 'W'+str(ft_WW)+'W'    

        if rep_ft_WW in tpl and '/Menge_Komplikation/' in tpl:
           tpl = tpl.replace(rep_ft_WW,'1')        
        #end of Menge_Komplikation

        #start of Menge_Operateur
        if tpl.count('V') == 2 and '/Menge_Operateur/' in tpl:
           ft_VV = tpl.split('V')[1]
           rep_ft_VV = 'V'+str(ft_VV)+'V'    

        if rep_ft_VV in tpl and '/Menge_Operateur/' in tpl:
           tpl = tpl.replace(rep_ft_VV,'1')        
        #end of Menge_Operateur

        
        #re.sub("[\[].*?[\]]", "[enty]", x) 
        #start of Bestrahlung
        #if tpl.count('(((') == 1 and tpl.count(')))') == 1 and tpl.count('[') == 0 and tpl.count(']') == 0 and '/Bestrahlung/' in tpl:
        #   tpl = tpl.replace('(((','[')
        #   tpl = tpl.replace(')))',']')
        #   tpl = re.sub("[\[].*?[\]]", "1", tpl)
        #   #ft_UU = tpl.split('U')[1]
        #   #rep_ft_UU = 'U'+str(ft_UU)+'U'    

        #if rep_ft_UU in tpl and '/Bestrahlung/' in tpl:
        #   tpl = tpl.replace(rep_ft_UU,'1')        
        #end of Bestrahlung

        
        #start of ST_Einzeldosis
        if tpl.count('T') == 2 and '/Einzeldosis/' in tpl:
           ft_TT = tpl.split('T')[1]
           rep_ft_TT = 'T'+str(ft_TT)+'T'    

        if rep_ft_TT in tpl and '/Einzeldosis/' in tpl:
           tpl = tpl.replace(rep_ft_TT,'1')        
        #end of ST_Einzeldosis
        

        #start of Residualstatus
        if tpl.count('S') == 2 and '/Residualstatus/' in tpl:
           ft_SS = tpl.split('S')[1]
           rep_ft_SS = 'S'+str(ft_SS)+'S'    

        if rep_ft_SS in tpl and '/Residualstatus/' in tpl:
           tpl = tpl.replace(rep_ft_SS,'1')        
        #end of Residualstatus

        #start of DatumSozialdienstkontakt
        if tpl.count('R') == 2 and '/DatumSozialdienstkontakt/' in tpl:
           ft_RR = tpl.split('R')[1]
           rep_ft_RR = 'R'+str(ft_RR)+'R'    

        if rep_ft_RR in tpl and '/DatumSozialdienstkontakt/' in tpl:
           tpl = tpl.replace(rep_ft_RR,'1')        
        #end of DatumSozialdienstkontakt

        #start of DatumStudienrekrutierung
        if tpl.count('Q') == 2 and '/DatumStudienrekrutierung/' in tpl:
           ft_QQ = tpl.split('Q')[1]
           rep_ft_QQ = 'Q'+str(ft_QQ)+'Q'    

        if rep_ft_QQ in tpl and '/DatumStudienrekrutierung/' in tpl:
           tpl = tpl.replace(rep_ft_QQ,'1')        
        #end of DatumStudienrekrutierung
        '''

        #start of Bestrahlung
        if tpl.count('(((') == 1 and tpl.count(')))') == 1 and tpl.count('[') == 0 and tpl.count(']') == 0:
           tpl = tpl.replace('(((','[')
           tpl = tpl.replace(')))',']')
           #using regular expression to fetch temporary id field
           tpl = re.sub("[\[].*?[\]]", "1", tpl)

        if tpl.count('*') == 2:
           mel_id = tpl.split('*')[1]
           if not mel_id in lst_mel_id:
              lst_mel_id.append(mel_id)
        #print('Formatting output file for Patient Id {} having Meldung Id {} \n \n'.format(pat_id,mel_id))

        if tpl.count('~') == 2:
           tumor_id = tpl.split('~')[1]

        ##start of formatting for Laborwert
        #if tpl.count("'") == 2:
        #   lbw_id = tpl.split("'")[1]

        if tpl.count('°') == 2:
           cTNM_id = tpl.split('°')[1]

        if tpl.count('ρ') == 2:
           pTNM_id = tpl.split('ρ')[1]

        MELID = str(mel_id)
        if 'MELID' in tpl:
           tpl = tpl.replace('MELID',MELID)

        if 'PAT_LABORWERT_ID' in tpl:
           tpl = tpl.replace('PAT_LABORWERT_ID',PAT_LABORWERT_ID)

        PAT_MELDUNGID = str(mel_id)
        #print('PAT_MELDUNGID is: ',PAT_MELDUNGID)
        PAT_MELDUNG_ID = str(mel_id) + '/' + str(tumor_id)
        rep_mel_id = '*'+str(mel_id)+'*'

        rep_tumor_id = '~'+str(tumor_id)+'~'
        rep_cTNM_id = '°'+str(cTNM_id)+'°'
        rep_pTNM_id = 'ρ'+str(pTNM_id)+'ρ'

        #fetching one of the Laborwert field to make it ID 
        if tpl.count("'") == 2:
           lbw_id = tpl.split("'")[1]
           if not str(lbw_id) in distinct_laborwert_lst:
              distinct_laborwert_lst.append(str(lbw_id))

        if tpl.count("'") == 2:
           lbw_id = tpl.split("'")[1]
        if len(distinct_laborwert_lst) > 0:
           idx_of_lab_typ = distinct_laborwert_lst.index(str(lbw_id))
        rep_lbw_id = "'"+str(lbw_id)+"'"
        if rep_lbw_id in tpl:
           tpl = tpl.replace(rep_lbw_id,str(idx_of_lab_typ+1))
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

       
        '''
        if 'MELID' in tpl and len(lst_mel_id)>0:
           tpl = tpl.replace('MELID', lst_mel_id[MELID_ctr])
           MELID_ind = 'T'
        if MELID_ind == 'T' and tpl=='\n' and MELID_ctr<len(lst_mel_id):
           MELID_ctr += 1
           MELID_ind = 'F'
        '''

        #print('PAT_MELDUNGID_ctr :',PAT_MELDUNGID_ctr)
        #print('length of lst_mel_id: ',len(lst_mel_id))
        #print('length of lst_mel_id is: ',len(lst_mel_id))
        if 'Tumorzuordnung/PAT_MELDUNGID' in tpl and len(lst_mel_id)>0:
           tpl = tpl.replace('Tumorzuordnung/PAT_MELDUNGID','Tumorzuordnung/'+lst_mel_id[PAT_MELDUNGID_ctr])
           #print('PAT_MELDUNGID replaced by',lst_mel_id[PAT_MELDUNGID_ctr])
           PAT_MELDUNGID_ind = 'T'
        if PAT_MELDUNGID_ind == 'T' and tpl=='\n' and PAT_MELDUNGID_ctr<len(lst_mel_id):
           PAT_MELDUNGID_ctr += 1
           PAT_MELDUNGID_ind = 'F'
        
        if 'DiagnoseFinding/PAT_MELDUNGID' in tpl and len(lst_mel_id)>0:
           tpl = tpl.replace('DiagnoseFinding/PAT_MELDUNGID','DiagnoseFinding/'+lst_mel_id[PAT_MELDUNGID_D_ctr])
           #print('PAT_MELDUNGID replaced by',lst_mel_id[PAT_MELDUNGID_D_ctr])
           PAT_MELDUNGID_D_ind = 'T'
        if PAT_MELDUNGID_D_ind == 'T' and tpl=='\n' and PAT_MELDUNGID_ctr<len(lst_mel_id):
           PAT_MELDUNGID_D_ctr += 1
           PAT_MELDUNGID_D_ind = 'F' 

        if 'OPReport/PAT_MELDUNGID' in tpl and len(lst_mel_id)>0:
           tpl = tpl.replace('OPReport/PAT_MELDUNGID','OPReport/'+lst_mel_id[PAT_MELDUNGID_O_ctr])
           #print('PAT_MELDUNGID replaced by',lst_mel_id[PAT_MELDUNGID_D_ctr])
           PAT_MELDUNGID_O_ind = 'T'
        if PAT_MELDUNGID_O_ind == 'T' and tpl=='\n' and PAT_MELDUNGID_O_ctr<len(lst_mel_id):
           PAT_MELDUNGID_O_ctr += 1
           PAT_MELDUNGID_O_ind = 'F' 

        '''
        if 'OPReport/O_PAT_MELDUNGID' in tpl and len(lst_opr_mel_id)>0:
           tpl = tpl.replace('OPReport/O_PAT_MELDUNGID','OPReport/'+str(lst_opr_mel_id[PAT_MELDUNGID_O_ctr]))
           #print('O_PAT_MELDUNGID replaced by',str(lst_opr_mel_id[PAT_MELDUNGID_O_ctr]))
           PAT_MELDUNGID_O_ind = 'T'
        if PAT_MELDUNGID_O_ind == 'T' and tpl=='\n' and PAT_MELDUNGID_O_ctr<len(lst_opr_mel_id):
           PAT_MELDUNGID_O_ctr += 1
           PAT_MELDUNGID_O_ind = 'F' 
        '''


        if 'PAT_MELDUNG_ID' in tpl:
           tpl = tpl.replace('PAT_MELDUNG_ID',PAT_MELDUNG_ID)

        #start of formatting for Melder_ID
        if rep_melder_id in tpl:
           tpl = tpl.replace(rep_melder_id,melder_id)

        if 'MELDER_ID' in tpl:
           tpl = tpl.replace('MELDER_ID',melder_id)

        #start of formatting for Absender_ID
        if rep_absender_id in tpl:
           tpl = tpl.replace(rep_absender_id,absender_id)

        if 'ABSENDER_ID' in tpl:
           tpl = tpl.replace('ABSENDER_ID',absender_id)

        #start of formatting for MENGE_HIST_ID
        if rep_menge_hist_id in tpl:
           tpl = tpl.replace(rep_menge_hist_id,menge_hist_id)

        if 'MENGE_HIST_ID' in tpl:
           tpl = tpl.replace('MENGE_HIST_ID',menge_hist_id)

        #start of formatting for tumor id
        if rep_tumor_id in tpl:
           tpl = tpl.replace(rep_tumor_id,tumor_id) 
  
        #start of formatting for cTNM id
        if 'CTNM_ID' in tpl:
           tpl = tpl.replace('CTNM_ID',str(cTNM_id))

        if rep_cTNM_id in tpl:
           tpl = tpl.replace(rep_cTNM_id,str(cTNM_id))


        #start of formatting for pTNM id
        if 'PTNM_ID' in tpl:
           tpl = tpl.replace('PTNM_ID',str(pTNM_id))

        if rep_pTNM_id in tpl:
           tpl = tpl.replace(rep_pTNM_id,str(pTNM_id))


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
    
    #Changes added on 10th May to resolve issue of MedicalVisit and Meldung while querying
    new_new_ttl_list = []
    for tpl in new_ttl_list:   
        for item in lst_mel_id:
            if '<https://fraunhofer.de/med2icin/ADT-GEKID/resources/MedicalVisit/'+str(item)+'> ' in tpl:
               tpl = tpl.replace('<https://fraunhofer.de/med2icin/ADT-GEKID/resources/MedicalVisit/'+str(item)+'> ', '<https://fraunhofer.de/med2icin/ADT-GEKID/resources/MedicalVisit/'+str(pat_id)+'> ')

        #changes added on 19 May 2021
        #fetching MFT ID
        if tpl.count('β') == 2:
           mft_id = tpl.split('β')[1]
        rep_mft_id = 'β'+str(mft_id)+'β'
        #end of changes added on 19 May 2021

        #changes added on 20th May 2021
        #fetching MOD MAMA ID
        if tpl.count('δ') == 2:
           mod_mama_id = tpl.split('δ')[1]
        rep_mod_mama_id = 'δ'+str(mod_mama_id)+'δ'
        #end of changes added on 20th May 2021



        new_new_ttl_list.append(tpl)
    new_ttl_list = new_new_ttl_list
    #End of changes added on 10th May to resolve issue of MedicalVisit and Meldung while querying

    #Changes added on 19th and 20th May to resolve MFT ID issue while querying
    new_new_ttl_list = []
    for tpl in new_ttl_list:   
        #start of formatting for MFT_ID
        if rep_mft_id in tpl:
           tpl = tpl.replace(rep_mft_id,mft_id)
        if 'MFT_ID' in tpl:
           tpl = tpl.replace('MFT_ID',mft_id)

        #start of formatting for Module_Mama_ID
        if rep_mod_mama_id in tpl:
           tpl = tpl.replace(rep_mod_mama_id,mod_mama_id)
        if 'MOD_MAMA_ID' in tpl:
           tpl = tpl.replace('MOD_MAMA_ID',mod_mama_id)

        new_new_ttl_list.append(tpl)
    new_ttl_list = new_new_ttl_list
    #End of changes added on 19th and 20th May to resolve MFT ID issue while querying

    #to remove repetitions, mainly of '\n'
    # e.g from [1,1,1,1,1,1,2,3,4,4,5,1,2] to [1, 2, 3, 4, 5, 1, 2]
    from itertools import groupby
    formated_ttl_list = [x[0] for x in groupby(new_ttl_list)]
    print('length of list is: ',len(formated_ttl_list))    

    f=open(final_out_path,'w')
    f.writelines(formated_ttl_list)
    f.close()
    return formated_ttl_list
