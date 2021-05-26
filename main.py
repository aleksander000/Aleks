import PySimpleGUI as sg
import json
import os
import shutil


token = ''
gname=[]
gid=[]
gcount=0
filename=""
group_dic={}
group_inv={}
group_orgid={}
newgrpname=""

inv_dic_id={}
inv_dic_type={}
inv_dic_orgid={}

org_dic_id={}

# **********************************************************************************************************************************************************

def get_org_inv():
    global inv_dic_id
    global inv_dic_type
    global inv_dic_orgid
    global org_dic_id
    global token #
    #
    #	tabsn=[0]
    #	tabip=[0]

    inv_dic_id.clear()
    inv_dic_type.clear()
    inv_dic_orgid.clear()
    org_dic_id.clear()


    pages = 1;
    newpage = ''
    ii = 0
    # Remove reort.csv if exists
    if os.path.exists("iventories.txt"):
        os.remove("inventories.txt")

    while (pages > 0):
        curlarg = 'curl -H "Authorization: Bearer ABCD1234567890abcd" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/invetories/?page_size=200" > inventories.json 2> null'
        print(curlarg)
        curlarg = 'curl -H "Authorization: Bearer ' + token + '" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/inventories/?page_size=200" > inventories.json 2> null'
#        print(curlarg)
        os.system(curlarg)
        pages = pages + 1
        newpage = '?page=' + str(pages);
        with open("inventories.json",encoding="utf-8") as json_file:
            data = json.load(json_file)
            x = str(data['next'])
            if x.find('=') < 0:
                pages = -4
 #           print(x)

            for p in data['results']:
                try:
                    y = str(p['id'])
                except IndexError:
                    y = 'NONE'

                try:
                    y1 = str(p['name'])
                except IndexError:
                    y1 = 'NONE'
                try:
                    y2 = str(p['kind'])  # if smart
                except IndexError:
                    y2 = 'NONE'
                try:
                    y3 = str(p['summary_fields']['organization']['name'])
                except IndexError:
                    y3 = 'NONE'
                try:
                    y4 = str(p['summary_fields']['organization']['id'])
                except IndexError:
                    y4 = 'NONE'

                f2 = open("inventories.txt", "a")
                f2.write(y1 + "," + y + "," + y2 + "," + y3 + "," + y4)
                f2.close

                org_dic_id[y3]=y4

                inv_dic_id[y1]=y
                inv_dic_type[y1]=y2
                inv_dic_orgid[y1]=y4

#                print(y1 + " | " + y + " | '" + y2 + "' | " + y3 + " | " + y4)
                print("ORG")
                print(org_dic_id)
                print("INV ID")
                print(inv_dic_id)
                print("INV Type")
                print(inv_dic_type)
                print("INV ORG")
                print(inv_dic_orgid)





# **********************************************************************************************************************************************************


def write2csv(arg1):
    arg1 = arg1 + '\n'
    f = open("report.csv", "a")
    f.write(arg1)
    f.close

# **********************************************************************************************************************************************************
def getreport():
    global token


    tabsn = [0]
    tabip = [0]


    pages = 1;
    newpage = ''
    ii = 0
    # Remove reort.csv if exists
    if os.path.exists("report.csv"):
        os.remove("report.csv")

# Write header to csv
    write2csv('Host ID,Host name,Hostname short,Enabled,Host IP,Host comment,Last job,Organization ID,Hosts VARs,Group ID,Group name,Group ID,Group name,Group ID,Group name,Group ID,Group name,Group ID,Group name,Group ID,Group name,Group ID,Group name,Group ID,Group name,Group ID,Group name,Group ID,Group name,Group ID,Group name,Group ID,Group name')

    while (pages > 0):
        if (pages == 1):
            curlarg = 'curl -H "Authorization: Bearer ABCD1234567890abcd" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/hosts/?page_size=200" > hosts.txt'
            print(curlarg)
            curlarg = 'curl -H "Authorization: Bearer ' + token + '" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/hosts/?page_size=200" > hosts.txt'
        else:
            curlarg = 'curl -H "Authorization: Bearer ABCD1234567890abcd" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/hosts/' + newpage + '&page_size=200" > hosts.txt'
            print(curlarg)
            curlarg = 'curl -H "Authorization: Bearer ' + token + '" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/hosts/' + newpage + '&page_size=200" > hosts.txt'
        os.system(curlarg)
        pages = pages + 1
        newpage = '?page=' + str(pages);
        with open("hosts.txt",encoding="utf-8") as json_file:
            data = json.load(json_file)
            if (pages == 2):
                allpages = 1 + int(int(data['count']) / 200)
            print("Pages ", pages, " of ", allpages)
            x = str(data['next'])
            if x.find('=') < 0:
                pages = -4
            print(x)

            for p in data['results']:
                try:
                    y = str(p['id'])
                except IndexError:
                    y = 'NONE'

                try:
                    y = y + "," + str(p['name'])
                except IndexError:
                    y = y + ',NONE'

                tabl = str(p['name']).split('.')
                shortname = tabl[0]
                y = y + "," + shortname  # short name

                try:
                    y = y + "," + str(p['enabled'])  # check if enabled
                except IndexError:
                    y = y + ',NONE'

                tabsn.append(str(shortname))

                # Here retore IP
                try:
                    yl = str(p['variables'])
                    ytab = yl.split("\n")
                    for yw in ytab:
                        if (not ('#' in yw)) and ('ansible_host:' in yw):
                            yw = yw.split()
                            # print (yw[1])
                            y = y + "," + str(yw[1])
                            tabip.append(str(yw[1]))
            # quit()
                except:
                    y = y + ',NONE'
                    tabip.append("NONE")

                try:
                    y = y + "," + str(p['description'])
                except IndexError:
                    y = y + ',NONE'

                try:
                    y1 = str(p['summary_fields']['last_job_host_summary']['failed'])
                except:
                    y1 = 'NONE'

            #			print (y1)
                if y1 == 'False':
                    y = y + ',O.K.'
                elif y1 == 'True':
                    y = y + ',Failed'
                else:
                    y = y + ',NONE'

            # Here Organization ID
                try:
                    y = y + "," + str(p['summary_fields']['inventory']['organization_id'])
                except IndexError:
                    y = y + ',NONE'

                try:
                    y = y + "," + str(p['variables'])
                    y = y.replace('\n', '|')
                except IndexError:
                    y = y + ',NONE'
                yk = 0
                maxgroup=16
                for yl in range(maxgroup):
                    try:
                        y = y + "," + str(p['summary_fields']['groups']['results'][yl]['id'])
                        y = y + "," + str(p['summary_fields']['groups']['results'][yl]['name'])
                    except:
                        for uu in range(maxgroup - yl):
                            y = y + ",NONE,NONE"
                        write2csv(y)
                        break
        if pages == -2:  # number of the pages limitation
           pages = -1


# **********************************************************************************************************************************************************
def groupdel(groupdelid):
    global token  #

    #    tcurlarg = 'curl -f -H "Authorization: Bearer ' + token + '" -H "Content-Type:application/json" -X DELETE -v -k "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/{' +str(groupdelid)+'}/" '
    tcurlarg = 'curl -f -H "Authorization: Bearer ' + token + '" -H "Content-Type:application/json" -X DELETE -v -k "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/{'+str(groupdelid)+'}/" 2> null'
    print(tcurlarg)
    print ("Start YYYXXX2")
    tstream = os.system(tcurlarg)
    print("return code = "+str(tstream))
    return int(tstream)


# ***********************************************************************************************************************************************************

def add2group(groupids, hostfile, invaddgrid):
    global token  #
    filetmp="tmp_out.tmp"
    # Check if group exists in Tower
#    curlarg = 'curl -H "Authorization: Bearer 8766989hjfhg" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/' + groupids + '/" 2> null'
    curlarg = 'curl -H "Authorization: Bearer 8766989hjfhg" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/'
    print(curlarg)
#    curlarg = 'curl -H "Authorization: Bearer ' + token + '" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/' + groupids + '/" 2> null 1> ' + filetmp
    curlarg = 'curl -H "Authorization: Bearer ' + token + '" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/' + groupids + '/" > ' + filetmp
    os.system(curlarg)
#    print(curlarg)

#    xstream = os.popen(curlarg)
#    lenoutpstr = str(xstream.read())
#    lenoutp = len(lenoutpstr.encode('utf8'))

    ftm=open(filetmp,"r", encoding="utf-8")
    lenoutpstr=ftm.readline()
    ftm.close()
    lenoutp = len(lenoutpstr)
    print("Size %d \n %s" % (lenoutp, lenoutpstr))
    if '"detail":"Not found."' in lenoutpstr:
       print("No group %s" % groupids)
       quit()
    print("it is")
    print ("Start with hostfile")
    xxq=0
    with open(hostfile,encoding="utf-8") as fp:
       for line in fp:
          xxq=xxq+1
          line = line.rstrip()
          tabline = line.split(".")

         # Here get host ID if exists
          hostn = tabline[0]
          hostn = hostn.lower()
          print(xxq,' : ',hostn)
#          curlarg = 'curl -H "Authorization: Bearer ' + token + '" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/hosts/?name__startswith=' + hostn + '" 2> null'
#          xstream = os.popen(curlarg)
#          lenoutpstr = str(xstream.read())
          curlarg = 'curl -H "Authorization: Bearer ' + token + '" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/inventories/{'+str(invaddgrid)+'}/hosts/?name__startswith=' + hostn + '" > ' + filetmp
          os.system(curlarg)
          ftm = open(filetmp, "r", encoding="utf-8")
          lenoutpstr = ftm.readline()
          ftm.close()



          liczba_hosts = lenoutpstr.split(',', 1)
          liczba_hosts = liczba_hosts[0].split(':')
          if int(liczba_hosts[1]) < 1:
              print("no host %s" % hostn)
              continue
          if int(liczba_hosts[1]) > 1:
              print("more than one host %s" % hostn)
              continue
          imdhosts = lenoutpstr.split('"id":', 2)
          imdhosts = imdhosts[1].split(',', 1)
          idhosts = imdhosts[0]
          if os.path.exists("payloadcrg.json"):
              os.remove("payloadcrg.json")
          fw = open("payloadcrg.json", "a")
          fw.write('{\n "id": ')
          fw.write(idhosts)
          fw.write('\n}')
          fw.close()
          tcurlarg = 'curl -f -H "Authorization: Bearer ' + token + '" -H "Content-Type:application/json" -X POST -d @payloadcrg.json  -v -k "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/{' + str(groupids) + '}/hosts/" 2> null'
#          print(tcurlarg)
#          print("Start XXX2")
          tstream = os.system(tcurlarg)

#         print ("groupadd")
#         quit()
    fp.close()


# ***********************************************************************************************************************************************************
# ***********************************************************************************************************************************************************
def addnewgroup (groupname,groupdescr,inventoryid):
    global token
    if os.path.exists("crgr.json"):
        os.remove("crgr.json")
    f = open("crgr.json", "a")
    f.write('{\n"inventory": ')
    f.write(str(inventoryid))
    f.write(',\n"name": "')
    f.write(groupname)
    f.write('",\n"description": "')
    f.write(groupdescr)
    f.write('"\n}')
    f.close()
#    quit()
    curlarg = 'curl -f -H "Authorization: Bearer TRSXC$#RTGF#&U" -H "Content-Type:application/json" -X POST -d @crgr.json  -v -k "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/"'
    print(curlarg)
    curlarg = 'curl -f -H "Authorization: Bearer ' + token + '" -H "Content-Type:application/json" -X POST -d @crgr.json  -v -k "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/"'
    print(curlarg)
    stream = os.popen(curlarg)
    outp = str(stream.read())
    textout=outp.encode('utf8')
    if len(textout) < 4:
       print ("server not created !")
       return(-1)
    else:
        print(textout)
        return(0)





# ***********************************************************************************************************************************************************
def del_hosts_from_group(groupa,filename1):
    global token
    with open(filename1) as fp:
        for line in fp:

            line = line.rstrip()
            tabline = line.split(".")

            # Here get host ID if exists
            hostn = tabline[0]
            hostn = hostn.lower()
            curlarg = 'curl -H "Authorization: Bearer ' + token + '" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/hosts/?name__startswith=' + hostn + '"'
            print(curlarg)
            #		os.system(curlarg)
            xstream = os.popen(curlarg)
            lenoutpstr = str(xstream.read())
            lenoutp = len(lenoutpstr.encode('utf8'))
            # print ("Size %d \n %s" % (lenoutp,lenoutpstr))
            liczba_hosts = lenoutpstr.split(',', 1)
            liczba_hosts = liczba_hosts[0].split(':')
            # print(liczba_hosts[1]);
            if int(liczba_hosts[1]) < 1:
                print("no host %s" % hostn)
                continue
            if int(liczba_hosts[1]) > 1:
                print("more than one host %s" % hostn)
                continue
            imdhosts = lenoutpstr.split('"id":', 2)
            imdhosts = imdhosts[1].split(',', 1)
            idhosts = imdhosts[0]
            print(hostn, " ", idhosts)
            idhosts = str(idhosts)

            # ******************************* DEL HostID from a group ****************************************************

            if os.path.exists("delhostfromgr.json"):
                os.remove("delhostfromgr.json")
            f = open("delhostfromgr.json", "a")
            f.write('{\n"id": ')
            f.write(idhosts)
            f.write(',\n"disassociate": 1\n}')
            f.close()
            tcurlarg = 'curl -f -H "Authorization: Bearer TRSXC$#RTGF#&U" -H "Content-Type:application/json" -X POST -d @delhostfromgr.json  -v -k "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/{' + str(groupa) + '}/hosts/"'
            print(tcurlarg)
            tcurlarg = 'curl -f -H "Authorization: Bearer ' + token + '" -H "Content-Type:application/json" -X POST -d @delhostfromgr.json  -v -k "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/{' + str(groupa) + '}/hosts/"'
            print(tcurlarg)
            tstream = os.system(tcurlarg)
            os.system(curlarg)
    fp.close()


# ***********************************************************************************************************************************************************
def get_hosts_from_group (groupa):
    global token
    pages = 1
    newpage = ''
    ii = 0
    # Remove reort.csv if exists
    if os.path.exists("reportgr.csv"):
        os.remove("reportgr.csv")

    # Write header to csv
    f1q = open("reportgr.csv", "a")
    f1q.write('Host ID,Host name, Short hostname, Inventory ID\n')
    f1q.close
    while (pages > 0):
        if (pages == 1):
            curlarg = 'curl -H "Authorization: Bearer ABCD1234567890abcd" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/{' + str(groupa) + '}/all_hosts/?page_size=200" > hostsgr.txt'
            print(curlarg)
            curlarg = 'curl -H "Authorization: Bearer ' + token + '" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/{' + str(groupa) + '}/all_hosts/?page_size=200" > hostsgr.txt'
        #		print (curlarg)
        else:
            curlarg = 'curl -H "Authorization: Bearer ABCD1234567890abcd" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/{' + str(groupa) + '}/all_hosts/' + newpage + '&page_size=200" > hostsgr.txt'
            print(curlarg)
            curlarg = 'curl -H "Authorization: Bearer ' + token + '" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/{' + str(groupa) + '}/all_hosts/' + newpage + '&page_size=200" > hostsgr.txt'
        #		print (curlarg)
        os.system(curlarg)
        #quit()
        pages = pages + 1
        newpage = '?page=' + str(pages);
        with open("hostsgr.txt") as json_file:
            data = json.load(json_file)
            if (pages == 2):
                allpages = 1 + int(int(data['count']) / 200)
            print("Pages ", pages, " of ", allpages)
            x = str(data['next'])
            if x.find('=') < 0:
                pages = -4
            print(x)

            for p in data['results']:
                try:
                    y = str(p['id'])
                except IndexError:
                    y = 'NONE'
                # Try for name of the hosts
                try:
                    y = y + "," + str(p['name'])
                except IndexError:
                    y = y + ',NONE'

                tabl = str(p['name']).split('.')
                shortname = tabl[0]
                y = y + "," + shortname  # short name

                # Try for inventory ID
                try:
                    y = y + "," + str(p['summary_fields']['inventory']['id'])
                except IndexError:
                    y = y + ',NONE'
                #			print ('Wynik linii = '+y)
                y = y + '\n'
                f1q.write(y)
        json_file.close()

        if pages == -2:  # number of the pages limitation
            pages = -1
    f1q.write('END\n')
    f1q.close


# ***********************************************************************************************************************************************************


def get_groups ():
    global gname
    global gid
    global gcount
    global group_dic
    global gname_vis
    global group_inv
    global group_orgid



    group_dic.clear()
    gname_vis.clear()
    group_inv.clear()
    group_orgid.clear()
    gname.clear()


    global token #
    pages = 1
    newpage = ''
    # Remove reort.csvgroups.txt if exists
    if os.path.exists("groups.txt"):
        os.remove("groups.txt")
    while (pages > 0):
 #       curlarg = 'curl -H "Authorization: Bearer ABCD1234567890abcd" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/?page_size=200" > groups.json 2> null'
 #       print(curlarg)
        curlarg = 'curl -H "Authorization: Bearer ' + token + '" --insecure -X GET "https://ansible-tower.ocp1.sr1.eu1.sp.ibm.local/api/v2/groups/?page_size=200" > groups.json 2> null'
        print(curlarg)
        os.system(curlarg)
        pages = pages + 1
        newpage = '?page=' + str(pages);
        with open("groups.json",encoding="utf-8") as json_file:
            data = json.load(json_file)
            x = str(data['next'])
            if x.find('=') < 0:
                pages = -4
            print(x)
            for p in data['results']:
                try:
                    y = str(p['id'])
                except IndexError:
                    y = 0
                gid.append(y)
                try:
                    y1 = str(p['name'])
                except IndexError:
                    y1 = 'NONE'
                try:
                    y2 = str(p['inventory'])
                except IndexError:
                    y2 = 'NONE'
                try:
                    y3 = str(p['summary_fields']['inventory']['organization_id'])
                except IndexError:
                    y3 = 'NONE'
                gname.append(y1)
                f = open("groups.txt", "a")
                f.write(y)
                f.write(y1)
                group_dic[y1] = y
                group_inv[y1] = y2
                group_orgid[y1] = y3
                f.close
                print(y1 + " | " + y)
            json_file.close()
    gname_vis.clear()
    for i in group_dic.keys():
        gname_vis.append(i)




# ***********************************************************************************************************************************************************
# ****************************************************** MAIN *****************************************************************************************
# ***********************************************************************************************************************************************************



#quit()


gname_vis=[]
org_vis=[]
inv_vis=[]

filename=" empty "
#groupdel(14007)

#quit()



get_groups ()


get_org_inv()

for i in org_dic_id.keys():
    org_vis.append(i)

for i in inv_dic_id.keys():
    if  "smart" not in inv_dic_type[i] :
        inv_vis.append(i)

#quit()

layout = [[sg.Combo(values=gname_vis,size=(70,10), enable_events=True, key='combo'),sg.Text(' Group Name')],
          [sg.Combo(values=inv_vis,size=(70,10), enable_events=True, key='combo_inv'),sg.Text(' Inventory Name')],
          [sg.Combo(values=org_vis,size=(7,10), enable_events=True, key='combo_org'),sg.Text(' Organization Name')],
          [sg.Button('Refresh'),sg.Button('Get Report'),sg.Button('Add hosts'),sg.Button('Add Group'), sg.Button('Del Group'), sg.Exit()],
          [sg.Button('Get group hosts'),sg.Button('Delete hosts in group')],
          [],
          [sg.Text('Filename = '+ filename, justification='c', size=(70,1), font='Mambo 15', key='-c-')],
          [sg.Input(key='_FILEBROWSE_', enable_events=True, visible=False)],
          [sg.Button('About'),sg.FileBrowse(target='_FILEBROWSE_')],
          [sg.Multiline('', size=(100,15), key='editor')],
          [sg.Button('Lowercase'), sg.Button('Endings'), sg.Button('localhost')],

          ]
window = sg.Window('Tower API more human accessor', layout, size=(700,580))
while True:
    event, values = window.Read()
    if event is None or event == 'Exit':
        break


    if event == 'combo_org':
        organid=org_dic_id[values['combo_org']]
        print(organid)
        inv_vis.clear()
        for keey in inv_dic_orgid:
            if organid in inv_dic_orgid[keey]:
                if 'smart' not in inv_dic_type[keey]:
                    inv_vis.append(keey)
        window.FindElement('combo_inv').Update(values=inv_vis,size=(70,10))
        gname_vis.clear()
        for keey in group_orgid:
            if organid in group_orgid[keey]:
                gname_vis.append(keey)
        window.FindElement('combo').Update(values=gname_vis,size=(70,10))

    if event == 'combo_inv':
        print(values['combo_inv'])
        invertorid=inv_dic_id[values['combo_inv']]
        print(invertorid)
        gname_vis.clear()
        for keey in group_inv:
            if invertorid in group_inv[keey]:
                gname_vis.append(keey)
        window.FindElement('combo').Update(values=gname_vis,size=(70,10))
        for keey in org_dic_id:
            if  org_dic_id[keey] == inv_dic_orgid[values['combo_inv']]:
                window.FindElement('combo_org').Update(keey)



    if event == 'combo':
        print(values['combo'])
        groupid=group_dic[values['combo']]
        for keey in org_dic_id:
            if org_dic_id[keey] == group_orgid[values['combo']]:
                window.FindElement('combo_org').Update(keey)
        for keey in inv_dic_id:
            if inv_dic_id[keey] == group_inv[values['combo']]:
                window.FindElement('combo_inv').Update(keey,size=(70,10))







    if event is not None :
        print(event, values)
        filename = values["_FILEBROWSE_"]
#        filename = filename.replace('/','\\')
        print(filename)
        window['-c-'].update(str(values["_FILEBROWSE_"]).replace('/','\\'))

    if event == 'Refresh':
        get_groups()
        print("Refresh")
        window.FindElement('combo').Update(values=gname_vis,size=(70,10))
 
 
    if event == 'Add hosts':
       try:
            invaddgrid=inv_dic_id[values['combo_inv']]
       except:
            sg.popup("No selected Inventory !")
            continue
       print(invaddgrid)
       combo = values['combo']  # use the combo key
       try:
           print(group_dic[combo])
       except :
           sg.popup("No selected group !")
           continue
       if not os.path.exists(filename):
           sg.popup("No file !")
           continue
       print(filename)
       print("add hosts")
#       continue
       add2group(group_dic[combo], filename, invaddgrid)
       sg.popup("You have added hosts to the group !")
#    window.FindElement('combo').Update(values=['a', 'b', 'c'])

    if event == 'Add Group':
        try:
            invaddgrid=inv_dic_id[values['combo_inv']]
        except:
            sg.popup("No selected Inventory !")
            continue
        print(invaddgrid)
        ewgrpname=' '
        ewgrpname=sg.popup_get_text("Name of the new group")
        if len(ewgrpname) < 4:
            sg.popup("Too short new group name !")
            continue

        ewgrpcom=' '
        ewgrpcom=sg.popup_get_text("Comment for the new group")
        if len(ewgrpcom) < 10:
            sg.popup("Too short new group comment !")
            continue
        if addnewgroup(ewgrpname,ewgrpcom,invaddgrid) == 0:
            sg.popup("Group created")
#            get_groups()
            print("Group created")
#            window.FindElement('combo').Update(values=gname_vis,size=(70,10))

        else:
            sg.popup_error("Group has not been created",title='Error during group creation')
#    window.FindElement('combo').Update(values=['a', 'b', 'c'])

    if event == 'Del Group':
        print ("deleting group")
        combo = values['combo']  # use the combo key
        try:
            i = group_dic[combo]
        except:
            sg.popup("No selected group !")
            continue
        print(i)
        #groupdel(i)
        sg.popup("You have deleted the group !")
    #    window.FindElement('combo').Update(values=['a', 'b', 'c'])

    if event == 'Get Report':
            file_report = sg.popup_get_text('Enter the Report filename')
            getreport()
            shutil.copyfile("report.csv", file_report)
            sg.popup("Asset report " + file_report + " has been created !")
    #    window.FindElement('combo').Update(values=['a', 'b', 'c'])

 #Get list of hosts in the group
    if event == 'Get group hosts':
        combo = values['combo']  # use the combo key
        try:
            i = group_dic[combo]
        except:
            sg.popup("No selected group !")
            continue
        print(i)
        file_report = sg.popup_get_text('Enter the Report of group Host filename')
        get_hosts_from_group(i)
        shutil.copyfile("reportgr.csv", file_report)
        sg.popup("Asset report " + file_report + " has been created !")
    #    window.FindElement('combo').Update(values=['a', 'b', 'c'])


    # Delete list of hosts from the group
    if event == 'Delete hosts in group':
        combo = values['combo']  # use the combo key
        try:
            i = group_dic[combo]
        except:
            sg.popup("No selected group !")
            continue
        print(i)
        if not os.path.exists(filename):
            sg.popup("No file !")
            continue
        del_hosts_from_group(i, filename)

# Change editor text to lowercase
    if event == 'Lowercase':
        tabedit_1=values['editor']
        tabedit=tabedit_1.splitlines()
        newedit=''
        for ll in tabedit:
            newedit=newedit+ll.lower()+'\n'
        window['editor'].update(newedit)
        print(newedit)

# Add etitor lines * ,
    if event == 'Endings':
        tabedit_1=values['editor']
        tabedit=tabedit_1.splitlines()
        newedit=''
        for ll in tabedit:
            if len(ll) < 4:
                continue
            ll = ll.strip()
            if '*' in ll:
                newedit = newedit + ll.lower() + '\n'
            else:
                newedit = newedit + ll.lower() + '* , \n'
        window['editor'].update(newedit)
        print(newedit)

# Add etitor lines * ,
    if event == 'localhost':
        tabedit_1 = values['editor']
        tabedit = tabedit_1.splitlines()
        newedit = ''
        flh=0
        for ll in tabedit:
            ll = ll.strip()
            if len(ll) < 4:
                continue
            if ('*' in ll) or ('localhost' in ll):
                newedit = newedit + ll.lower() + '\n'
            else:
                newedit = newedit + ll.lower() + '* , \n'
            if ('localhost' in ll):
                flh=1
        if  flh == 0:
            newedit = newedit + 'localhost'
        window['editor'].update(newedit)
        print(newedit)

    if event == 'About':
       sg.popup("Version 1.3.2 May 25th 2021 \n made by Aleksander Kisiel \n aleksander.kisiel@pl.ibm.com",title="About")
#    window.FindElement('combo').Update(values=['a', 'b', 'c'])


window.Close()

