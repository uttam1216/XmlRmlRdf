
v1: Pateint address added. Shows details of 30 patients and thier addreses.

v2: Upon adding other triples conditions in where clause, only 27 rows appear instead of earlier 30 records.
v3: Menge_OP if kept in OPTIONAL, restores the issue and again 30 rows are displayed.

v4: Melder details are also fetched and conditions for them are also mentioned in where clause, however, the number of records get doubled.

v5: All fields including patient address and melder details are added to original query.
v6: Melder and Menge_OP are made OPTIONAL to get final improved results.

Note: Melder is not related to patient, so select it separately.

19 May, 2021:
5 more fields(MelderAdresse, Melder_Bankname, Melder_BIC, Melder_IBAN, Melder_Kontoinhaber) related to Absender as present in the defined ontology added (earlier was missed as it was not present in the Testperson.xml file)
New query made to fetch Absender details. (since it is not a part of patient)
New query made to fetch Melder details. (since it is not a part of patient)
Rules file and python formatting script changed to adhere to correct Absender and Melder mapping as per ontology.
