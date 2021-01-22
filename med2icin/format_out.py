import re

def process_out_file(inp_file_name):
    inp_file_path = 'output_files/' + inp_file_name
    final_out_path = 'final_output_files/' + inp_file_name.replace('.ttl','') + '_final.ttl'
    with open(inp_file_path) as f:
        lines = f.readlines()
    lines_lst = lines
    pat_id = 0
    mel_id = 0
    addr_plz = 0
    for tpl in lines_lst:
        if tpl.count('+') == 2:
           pat_id = tpl.split('+')[1]
        if tpl.count('*') == 2:
           mel_id = tpl.split('*')[1]
        if tpl.count('!') == 2:
           addr_plz = tpl.split('!')[1]
    print(pat_id)
    print(mel_id)
    print(addr_plz)
    PAT_ADDR_ID = pat_id + '/1'
    PAT_MELDUNGID = mel_id
    PAT_MELDUNG_ID = str(mel_id) + '/1'
    rep_pat_id = '+'+str(pat_id)+'+'
    rep_mel_id = '*'+str(mel_id)+'*'
    rep_addr_plz = '!'+str(addr_plz)+'!'
    new_ttl_list = []
    for tpl in lines_lst:
        if rep_pat_id in tpl:
           tpl = tpl.replace(rep_pat_id,pat_id)
        if rep_mel_id in tpl:
           tpl = tpl.replace(rep_mel_id,mel_id)
        if rep_addr_plz in tpl:
           tpl = tpl.replace(rep_addr_plz,PAT_ADDR_ID)
        if 'PAT_ADDR_ID' in tpl:
           tpl = tpl.replace('PAT_ADDR_ID',PAT_ADDR_ID)
        if 'PAT_MELDUNGID' in tpl:
           tpl = tpl.replace('PAT_MELDUNGID',PAT_MELDUNGID)
        if 'PAT_MELDUNG_ID' in tpl:
           tpl = tpl.replace('PAT_MELDUNG_ID',PAT_MELDUNG_ID)
        if 'PAT_ID' in tpl:
           tpl = tpl.replace('PAT_ID',pat_id)
        new_ttl_list.append(tpl)
    new_ttl_list.reverse()
    f=open(final_out_path,'w')
    f.writelines(new_ttl_list)
    f.close()
    return new_ttl_list
