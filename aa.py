botslocation = []  # record all bots locations
    remainbots = client.bots  # record number of bots unfounded yet
    h = client.home  # home
    all = set([i for i in range(client.v)])
    visited = set([h])  # visited vertices set
    unvisited = all - visited  # unvisited vertices set
    xx = [1 / client.students] * (client.students)  # Multi-Weight:x
    weight = xx.copy()  # Multi-Weight:weight

    ##first iertation: find the nearest neighbor from h
    mindis1 = inf
    v1 = 0  # store nearest neighbor from h
    for vv in findneighbour(client, map1, h):
        if map1[vv][h] < mindis1:
            mindis1 = map1[vv][h]
            v1 = vv
            break
    visited.add(v1)  # add v1 into visited set

    ##first iteration: scout, remote and update
    weightsum = 0
    claim = client.scout(v1, all_students)
    if client.remote(v1, h) == None:
        for stu in range(client.students):
            if claim[stu+1] == True:
                weight[stu] = weight[stu] * (1 - epsilon)
            weightsum += weight[stu]
        for stu in range(client.students):
            xx[stu] = weight[stu] / weightsum
    else:
        botslocation.append(h)
        remainbots -= 1
        for stu in range(client.students):
            if claim[stu+1] == False:
                weight[stu] = weight[stu] * (1 - epsilon)
            weightsum += weight[stu]
        for stu in range(client.students):
            xx[stu] = weight[stu] / weightsum
    ##pick next vertex:
    while remainbots > 0:
        maxvote = 0 #mark the maximum score that a bot will be there
        un = 0  #unvisited vertex
        vn = 0  #visited vertex
        ##find the most possible vertex that a bot will be there
        for v in visited:
            for u in unvisited:
                if u in findneighbour(client, map1, v):
                    claim = client.scout(u, all_students)
                    currvote = 0    #mark the current score that a bot will be there
                    for stu in range(client.students):
                        if claim[stu+1] == True:
                            currvote += xx[stu]
                    if currvote > maxvote:
                        maxvote = currvote
                        vn = v
                        un = u
        visited.add(un)
        unvisited.remove(un)
        claim = client.scout(un, all_students)
        if client.remote(un, vn) == None:
            for stu in client.students:
                if claim[stu+1] == True:
                    weight[stu] = weight[stu] * (1 - epsilon)
                weightsum += weight[stu]
            for stu in range(client.students):
                xx[stu] = weight[stu] / weightsum
        else:
            botslocation.append(vn)
            remainbots -= 1
            for stu in client.students:
                if claim[stu+1] == False:
                    weight[stu] = weight[stu] * (1 - epsilon)
                weightsum += weight[stu]
            for stu in client.students:
                xx[stu] = weight[stu] / weightsum