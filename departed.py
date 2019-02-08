import sys
import ldap
import pandas as pd

all_departed_accounts = []
departed=[]
array=[]
LDAP_SERVER = "<ldap_server_ip>"
BASE_DN = "DC=<parent>,DC=<child>"
BASE_SEARCH_DN_DEPARTED_USERS = "OU=<child3>,OU=<child2>,DC=<child1>,DC=<parent>"
LDAP_FILTER_DEPARTED = "(&(objectClass=user)(objectClass=person))"
LDAP_USER = ""
LDAP_PASSWD = ""
LDAP_ATTRIBUTES = [ "sAMAccountName"]

ldap_connection = ldap.initialize('ldap://' + LDAP_SERVER)
ldap_connection.protocol_version = 3
ldap_connection.set_option(ldap.OPT_REFERRALS, 0)
ldap_connection.simple_bind_s(LDAP_USER, LDAP_PASSWD)



#get info on accounts 
ldap_result_id=ldap_connection.search_ext(BASE_SEARCH_DN_DEPARTED_USERS,ldap.SCOPE_SUBTREE,LDAP_FILTER_DEPARTED,LDAP_ATTRIBUTES,sizelimit=4000)
try:
	while 1:
		result_type,result_data=ldap_connection.result(ldap_result_id,0)
		if(result_data==[]):
			break
		else:
			if result_type==ldap.RES_SEARCH_ENTRY:
				array.append(result_data[0][1])
				
except ldap.SIZELIMIT_EXCEEDED:
	print "Limit exceeded"
departed=[a.values()[0] for a in array]
all_departed_accounts=[val for sublist in departed for val in sublist] 
#print ','.join(repr(p) for p in all_departed_accounts)


df=pd.DataFrame(all_departed_accounts,columns=["<field_name>"])
df.to_csv('<output_csv>',index=False)

