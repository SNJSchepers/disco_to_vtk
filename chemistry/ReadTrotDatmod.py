def ReadTrotDatmod(filename=None):
    
    import numpy as np
    
    # Generated with SMOP  0.41
    # ReadTrotDatmod.m
    #
    
    # @function
    # def ReadTrotDatmod(filename=None):
        # Function ReadThermDat reads properties from ALEX chemistry file
    #  Output: El
    #              El.Name
    #              El.Mass
    #          Sp
    #              Sp.Name
    #              Sp.Mass
    #              Sp.pol  [2x8]     JANAF polynimials for Thermodynamic data
    #              Sp.visc [var]     Polnomial coefficients for viscosity
    #              Sp.viscord        Order of viscosity polynomial
    #              Sp.cond [var]     Polnomial coefficients for conductivity
    #              Sp.condord        Order of conductivity polynomial
    #              Sp.diff [NspxNsp] Polynomial coefficients for binary 
    #                                diffusion coefficients
    #          Both structs(in matlab)! Here in Python both are lists of dictionaries!
    show = True
    
    fid=open(filename)
    # ReadTrotDatmod.m:20
    SFP=fid.tell()
    Keys = [dict() for x in range(7)]
    # ReadTrotDatmod.m:21
    
    Ready=0
    # ReadTrotDatmod.m:22
    Keys[0]["Name"] = 'ELEM'
    # ReadTrotDatmod.m:23
    Keys[1]["Name"] = 'SPEC'
    # ReadTrotDatmod.m:24
    Keys[2]["Name"] = 'THERMO'
    # ReadTrotDatmod.m:25
    Keys[3]["Name"] = 'VISCOSITY'
    # ReadTrotDatmod.m:26
    Keys[4]["Name"] = 'CONDUCTIVITY'
    # ReadTrotDatmod.m:27
    Keys[5]["Name"] = 'DIFFUSIVITIES'
    # ReadTrotDatmod.m:28
    Keys[6]["Name"] = 'REAC'
    # ReadTrotDatmod.m:29
    Found=0
    # ReadTrotDatmod.m:30
    iKey=0
    # ReadTrotDatmod.m:30
    NumKeys=len(Keys)
    # ReadTrotDatmod.m:30
    while (iKey < NumKeys):
    
        fid.seek(SFP,0)
        # fid.seek(360,0)
        CurKey=Keys[iKey]["Name"]
        # ReadTrotDatmod.m:33
        KeyLength=len(CurKey)
        # ReadTrotDatmod.m:34
        while (Found == 0):
            CFP=fid.tell()
            # ReadTrotDatmod.m:36
            CurLine=fid.readline(); # fgetl(fid)
            if not CurLine:
                # print("feof")
                break
            # ReadTrotDatmod.m:37
            # print(CurLine, CFP)
            LineLength=len(CurLine)
            # ReadTrotDatmod.m:37
            Lend=min(KeyLength + 5,LineLength)
            # ReadTrotDatmod.m:38
            Matches=CurLine.find(CurKey,0,Lend)
            # ReadTrotDatmod.m:39
            if (Matches > -1 and LineLength > KeyLength):
                Found=1
                # ReadTrotDatmod.m:41
                iKey=iKey + 1
                # ReadTrotDatmod.m:42
            del Matches
        # print(Found)
        if (Found == 1):
            fid.seek(CFP,0)
            if 'ELEM' == CurKey:
                CurLine=fid.readline()
                columns=CurLine.split()
                # ReadTrotDatmod.m:50
                Ne=int(columns[1])
                El = [dict() for x in range(Ne)]
                # ReadTrotDatmod.m:51
                if show:
                    print("Processing ",columns,": ",Ne," entries")
                for curEl in El:
                    CurLine=fid.readline()
                    columns=CurLine.split()
                    curEl["Name"] = columns[0]
                    # ReadTrotDatmod.m:56
                    curEl["Mass"] = float(columns[1])
                ElNames = [El[x]["Name"] for x in range(Ne)]
                # ReadTrotDatmod.m:57
            elif 'SPEC' == CurKey:
                CurLine=fid.readline()
                columns=CurLine.split()
                Nsp=int(columns[1])
                # ReadTrotDatmod.m:60
                # ReadTrotDatmod.m:61
                Sp = [dict() for x in range(Nsp)]
                if show:
                    print("Processing ",columns,": ",Nsp," entries")
                for curSp in Sp:
                    CurLine=fid.readline()
                    columns=CurLine.split()
                    curSp["Name"] = columns[0]
                    # ReadTrotDatmod.m:66
            elif 'REAC' == CurKey:
                Nreac=int(fid.readline().split()[1])
                # ReadTrotDatmod.m:70
                if show:
                    print("Processing ",columns,": ",Nreac," entries")
                Diaz=fid.readline().split()[0]
                # ReadTrotDatmod.m:74
                
                SpNames = [Sp[x]["Name"] for x in range(Nsp)]
                SpNames.append('M')
                
                Re = [dict() for x in range(Nreac)]
                for curRe in Re:
                    columns=fid.readline().split()
                    ireac=int(columns[0])
                    # ReadTrotDatmod.m:76
                    ifile=int(columns[1])
                    # ReadTrotDatmod.m:77
                    iline=int(columns[2])
                    # ReadTrotDatmod.m:78
                    rev=columns[3]
                    # ReadTrotDatmod.m:79
                    if rev == 'REV':
                        curRe["rev"] = True
                        # ReadTrotDatmod.m:81
                    elif rev == 'IRREV':
                        curRe["rev"] = False
                        # ReadTrotDatmod.m:83
                    elif show:
                        print('Unknown value')
                    pdep=columns[4]
                    # ReadTrotDatmod.m:87
                    if pdep == 'PDEP':
                        curRe["pdep"] = True
                        # ReadTrotDatmod.m:81
                    elif pdep == 'INDEP':
                        curRe["pdep"] = False
                        # ReadTrotDatmod.m:83
                    elif show:
                        print('Unknown value')
                    
                    third=columns[5]
                    # ReadTrotDatmod.m:96
                    ford = int(fid.readline().split()[0])
                    columns = fid.readline().split()
                    # ReadTrotDatmod.m:98
                    ihlp = 0
                    curRe["fspec"] = np.zeros(ford, dtype=int)
                    curRe["fstoi"] = np.zeros(ford, dtype=int)
                    curRe["fpow"] = np.zeros(ford, dtype=int)
                    for i in np.arange(0,ford):
                        nu=int(columns[ihlp]); ihlp+=1
                        # ReadTrotDatmod.m:100
                        pow=int(columns[ihlp]); ihlp+=1
                        # ReadTrotDatmod.m:101
                        Name=columns[ihlp]; ihlp+=1
                        # ReadTrotDatmod.m:102
                        curRe["fspec"][i] = SpNames.index(Name)
                        # ReadTrotDatmod.m:103
                        curRe["fstoi"][i] = nu
                        # ReadTrotDatmod.m:104
                        curRe["fpow"][i] = pow
                        # ReadTrotDatmod.m:105
                    
                    rord = int(fid.readline().split()[0])
                    columns = fid.readline().split()
                    ihlp = 0
                    curRe["rspec"] = np.zeros(rord, dtype=int)
                    curRe["rstoi"] = np.zeros(rord, dtype=int)
                    curRe["rpow"] = np.zeros(rord, dtype=int)
                    # ReadTrotDatmod.m:108
                    for i in np.arange(0,rord):
                        nu=int(columns[ihlp]); ihlp+=1
                        # ReadTrotDatmod.m:110
                        pow=int(columns[ihlp]); ihlp+=1
                        # ReadTrotDatmod.m:111
                        Name=columns[ihlp]; ihlp+=1
                        # ReadTrotDatmod.m:112
                        curRe["rspec"][i] = SpNames.index(Name)
                        # ReadTrotDatmod.m:113
                        curRe["rstoi"][i] = nu
                        # ReadTrotDatmod.m:114
                        curRe["rpow"][i] = pow
                        # ReadTrotDatmod.m:115
                    # Arrhenius coefficients
                    columns = fid.readline().split()
                    curRe["preexp"] = float(columns[0])
                    # ReadTrotDatmod.m:119
                    curRe["Tpower"] = float(columns[1])
                    # ReadTrotDatmod.m:120
                    curRe["Tactivation"] = float(columns[2])
                    # ReadTrotDatmod.m:121
                    columns = fid.readline().split()
                    Check = columns[0]
                    # ReadTrotDatmod.m:123
                    if Check == Diaz or Check == 'END':
                        auxinfo=False
                        # ReadTrotDatmod.m:125
                    else:
                        auxinfo=True
                        # ReadTrotDatmod.m:127
                    curRe["revgiven"] = False
                    # ReadTrotDatmod.m:130
                    curRe["revdata"] = np.zeros(0, dtype=float)
                    # ReadTrotDatmod.m:131
                    curRe["enhanced"] = False
                    # ReadTrotDatmod.m:132
                    curRe["enhspec"] = np.zeros(0, dtype=int)
                    # ReadTrotDatmod.m:133
                    curRe["enhval"] = np.zeros(0, dtype=float)
                    # ReadTrotDatmod.m:134
                    curRe["low"] = False
                    # ReadTrotDatmod.m:135
                    curRe["lowdata"] = np.zeros(0, dtype=float)
                    # ReadTrotDatmod.m:136
                    curRe["troe"] = False
                    # ReadTrotDatmod.m:137
                    curRe["troedata"] = np.zeros(0, dtype=float)
                    # ReadTrotDatmod.m:138
                    curRe["sri"] = False
                    # ReadTrotDatmod.m:139
                    curRe["sridata"] = np.zeros(0, dtype=float)
                    # ReadTrotDatmod.m:140
                    curRe["dup"] = False
                    # ReadTrotDatmod.m:141
                    while auxinfo:
                
                        if Check == 'REV':
                            curRe["revgiven"] = True
                            # ReadTrotDatmod.m:145
                            curRe["revdata"] = np.array([float(x) for x in fid.readline().split()])
                            # ReadTrotDatmod.m:146
                        elif Check == 'ENHANCED':
                            curRe["enhanced"] = True
                            # ReadTrotDatmod.m:148
                            Nenh=int(columns[1])
                            curRe["enhspec"] = np.zeros(Nenh, dtype=int)
                            curRe["enhval"] = np.zeros(Nenh, dtype=float)
                            # ReadTrotDatmod.m:149
                            for i in np.arange(0,Nenh):
                                columns = fid.readline().split()
                                Name = columns[0]
                                # ReadTrotDatmod.m:151
                                val = float(columns[1])
                                # ReadTrotDatmod.m:152
                                curRe["enhspec"][i] = SpNames.index(Name)
                                # ReadTrotDatmod.m:153
                                curRe["enhval"][i] = val
                                # ReadTrotDatmod.m:154
                        elif Check == 'LOW':
                            curRe["low"] = True
                            # ReadTrotDatmod.m:157
                            curRe["lowdata"] = np.array(columns[1:],dtype=float)
                            # ReadTrotDatmod.m:158
                        elif Check == 'TROE':
                            curRe["troe"] = True
                            # ReadTrotDatmod.m:160
                            Ntroe=int(columns[1])
                            # ReadTrotDatmod.m:161
                            curRe["troedata"] = np.array(columns[2:2+Ntroe],dtype=float)
                            # ReadTrotDatmod.m:162
                        elif strcmp(Check,'SRI'):
                            curRe["sri"] = True
                            # ReadTrotDatmod.m:164
                            curRe["sridata"] = np.array(columns[1:7],dtype=float)
                            # ReadTrotDatmod.m:165
                        elif strcmp(Check,'DUP'):
                            curRe["dup"] = True
                            # ReadTrotDatmod.m:167
                        elif show:
                            print('Unknown auxiliary information')
                        columns = fid.readline().split()
                        Check = columns[0]
                        # ReadTrotDatmod.m:172
                        if Check == Diaz or Check == 'END':
                            auxinfo = False
                            # ReadTrotDatmod.m:174
                        else:
                            auxinfo = True
                            # ReadTrotDatmod.m:176
                
                    if third in [Sp[x]["Name"] for x in range(Nsp)]:
                        # third body which is not "M"
                        Re(k).enhanced = copy(true)
                        # ReadTrotDatmod.m:181
                        Re(k).enhspec = copy(setdiff(arange(1,Nsp),find(strcmp(third,cellarray([Sp.Name])))))
                        # ReadTrotDatmod.m:182
                        Re(k).enhval = copy(zeros(1,Nsp - 1))
                # ReadTrotDatmod.m:183
            elif 'THERMO' == CurKey:
                CurLine=fid.readline()
                columns=CurLine.split()
                # ReadTrotDatmod.m:187
                Nsp=int(columns[1])
                # ReadTrotDatmod.m:188
                if show:
                    print("Processing ",columns,": ",Nsp," entries")
                for ii in np.arange(0,Nsp):
                    # SkipLine=fgetl(fid)
                    CurLine=fid.readline()
                    # ReadTrotDatmod.m:193
                    CurLine=fid.readline()
                    # Name=fscanf(fid,'%s\n',concat([1,1]))
                    Name=CurLine.split()[0]
                    # ReadTrotDatmod.m:194
                    Phase=fid.readline().split()[0]
                    # ReadTrotDatmod.m:195
                    columns=fid.readline().split()
                    # CurNel=fscanf(fid,'%i\n',concat([1,1]))
                    CurNel=int(columns[0])
                    # ReadTrotDatmod.m:197
                    # comp=zeros(size(concat([El.Mass])))
                    comp=np.zeros(Ne, dtype=int)
                    # ReadTrotDatmod.m:199
                    for i in np.arange(0,CurNel):
                        comp[ElNames.index(columns[2*i+1])] = int(columns[2*i+2])
                    # ReadTrotDatmod.m:205
                    # ReadTrotDatmod.m:209
                    Sp[ii]["Mass"] = float(fid.readline().split()[1])
                    # ReadTrotDatmod.m:210
                    CurLine=fid.readline()
                    # ReadTrotDatmod.m:211
                    T1range=np.array([float(x) for x in fid.readline().split()])
                    # ReadTrotDatmod.m:212
                    Cp1=np.concatenate((np.array([float(x) for x in fid.readline().split()]), \
                        np.array([float(x) for x in fid.readline().split()])))
                    # ReadTrotDatmod.m:213
                    T2range=np.array([float(x) for x in fid.readline().split()])
                    # ReadTrotDatmod.m:214
                    Cp2=np.concatenate((np.array([float(x) for x in fid.readline().split()]), \
                        np.array([float(x) for x in fid.readline().split()])))
                    # ReadTrotDatmod.m:215
                    Sp[ii]["Ts"] = T1range[1]
                    # ReadTrotDatmod.m:216
                    Sp[ii]["pol"] = np.copy(np.concatenate((Cp1,Cp2)).reshape(2,-1))
                    # ReadTrotDatmod.m:217
                    Sp[ii]["elcomp"] = np.copy(comp)
                    # ReadTrotDatmod.m:218
                    Sp[ii]["phase"] = np.copy(Phase)
                    # ReadTrotDatmod.m:219
                    Sp[ii]["Comment"] = np.copy(fid.readline())
                    # ReadTrotDatmod.m:220
                
            elif 'VISCOSITY' == CurKey:
                CurLine=fid.readline()
                columns=CurLine.split()
                # ReadTrotDatmod.m:223
                Nsp=int(columns[1])
                # ReadTrotDatmod.m:224
                if show:
                    print("Processing ",columns,": ",Nsp," entries")
                for ii in np.arange(0,Nsp):
                    CurLine=fid.readline()
                    Name=CurLine.split()[0]
                    # ReadTrotDatmod.m:229
                    Ord=int(CurLine.split()[1])
                    # ReadTrotDatmod.m:230
                    Sp[ii]["viscord"] = np.copy(Ord)
                    # ReadTrotDatmod.m:231
                    Sp[ii]["visc"] = np.copy(np.array([float(x) for x in CurLine.split()[2:]]))
                    # ReadTrotDatmod.m:232
            elif 'CONDUCTIVITY' == CurKey:
                CurLine=fid.readline()
                columns=CurLine.split()
                # ReadTrotDatmod.m:235
                Nsp=int(columns[1])
                # ReadTrotDatmod.m:236
                if show:
                    print("Processing ",columns,": ",Nsp," entries")
                for ii in np.arange(0,Nsp):
                    CurLine=fid.readline()
                    Name=CurLine.split()[0]
                    # ReadTrotDatmod.m:241
                    Ord=int(CurLine.split()[1])
                    # ReadTrotDatmod.m:242
                    Sp[ii]["condord"] = np.copy(Ord)
                    # ReadTrotDatmod.m:243
                    Sp[ii]["cond"] = np.copy(np.array([float(x) for x in CurLine.split()[2:]]))
                    # ReadTrotDatmod.m:244
            elif 'DIFFUSIVITIES' == CurKey:
                # Check=fscanf(fid,'%s',concat([1,1]))
                CurLine=fid.readline()
                columns=CurLine.split()
                # ReadTrotDatmod.m:247
                Nsp=int(columns[1])
                # ReadTrotDatmod.m:248
                if show:
                    print("Processing ",columns,": ",Nsp," entries")
                for ii in np.arange(0,Nsp):
                    Sp[ii]["difford"] = np.zeros((Nsp,), dtype=int)
                    Sp[ii]["diff"] = np.zeros((Nsp,10))
                    for jj in np.arange(0,ii+1):
                        CurLine=fid.readline()
                        Name1=CurLine.split()[0]
                        # ReadTrotDatmod.m:254
                        Name2=CurLine.split()[1]
                        # ReadTrotDatmod.m:255
                        Ord=int(CurLine.split()[2])
                        # ReadTrotDatmod.m:256
                        Sp[ii]["difford"][jj] = np.copy(Ord)
                        # ReadTrotDatmod.m:257
                        # ReadTrotDatmod.m:258
                        Sp[ii]["diff"][jj][0:Ord] = np.copy(np.array([float(x) for x in CurLine.split()[3:]]))
                        # ReadTrotDatmod.m:259
                # Mirror the matrix D_ij=D_ji
                for ii in np.arange(0,Nsp):
                    for jj in np.arange(ii + 1,Nsp):
                        Sp[ii]["difford"][jj]=Sp[jj]["difford"][ii]
                        # ReadTrotDatmod.m:266
                        Sp[ii]["diff"][jj][:] = Sp[jj]["diff"][ii][:]
                        # ReadTrotDatmod.m:267
            else:
                if show:
                    print('Yet undefined case: [',CurKey,']')
            Found=0
            # ReadTrotDatmod.m:275
        else:
            if show:
                print(CurKey," NOT found")
                print("Apparently invalid!")
            iKey=iKey + 1
    # ReadTrotDatmod.m:281
    
    fid.close
    #
    Nel = Ne
    Nre = Nreac
    
    #  returning the final dictionary lists and their lengths
    return El, Sp, Re, Nel, Nsp, Nre
