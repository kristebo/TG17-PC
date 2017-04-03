import csv

participants = open('participants.txt','r') # partid, sum
tasksdone = open('tasksdone.txt','r') #taskname, partids

rowstask=[]
def get_participant_total(partid):
    #return the sum for this partid and taskids.
    #partid, sum
    #read rows in participants.txt
    participantslist=[]
    fields=("partid", "sum")
    rowsparts=csv.DictReader(participants, fields)
    for row in rowsparts:
        participantslist.append(row)
    for p in participantslist:
        #print p
        if p.get('partid')==partid:
            return p #jsonify({'participant':p})
    return -1


def get_taskstate(tasknr):
    #return the praticipants that have done this task and succeeded.
    # _id, [partids]
    fieldst=("taskname", "participants")
    rowstaskt=csv.DictReader(tasksdone, fieldst)
    for row in rowstaskt:
        #print row
        rowstask.append(row)
    return repr(rowstask[tasknr-1]) # jsonify({'taskstate':rowstask[tasknr-1]})

print get_participant_total('joms')

print get_taskstate(1)
