# ~~~~~~пересчет power много берет *****
# ~~~~~~оптимизировать scan??? **
# ~~~~~~конкатенация заменена ***
# ~~~~~~король бегает
# ~~~~~~ферзь в начале
# !!!!! алгоритм !!!!!! черные ходят, смотрят максимальное отношение ч. к б. после хода белых, которые смотрят минимальное отношение ч. к б. и т.д. Т.е. отбирается максимум из самой неблагоприятной ситуации для черных
# !!!!! проблема с черным ферзем. ходит так, что его на следующих ход рубят, однако в mx не написано такого (mx = black/white). mx>1 показывает
# сделать показатель адекватности хода игрока сразу (как-то сохранить результат)
# сохранять будущие ходы (dict dict-ов dict-ов?)
# сделать для пешек отдельный mult
# слишком много ест алгоритм бота. возвращается куча значений. не все нужны (random?) боту доступно примерно 30 ходов. т.е. с глубиной мысли в 2 полных хода (2б 2ч) это 30^4, а с 10 полными ходами 30^20

black_bg="\033[40m"
white_bg="\033[47m"
reset="\033[0m"
white_txt="\033[037m"
black_txt="\033[030m"
red_bg="\033[041m"

figs=["♔","♕","♖","♗","♘","♙","♚","♛","♜","♝","♞","♟"," "]
cost=[10_000,9,5,3,3,1,10_000,9,5,3,3,1,0]
for i in range(6): figs[i]=white_txt+figs[i]
for i in range(6,12): figs[i]=black_txt+figs[i]
begin=[[[4,7]],[[3,7]],[[0,7],[7,7]],[[2,7],[5,7]],[[1,7],[6,7]],[[i,6] for i in range(8)],[[4,0]],[[3,0]],[[0,0],[7,0]],[[2,0],[5,0]],[[1,0],[6,0]],[[i,1] for i in range(8)]]
doska=[[" " for x in range(8)] for y in range(8)]
for figura in range(12):
    for tochka in begin[figura]:
        doska[tochka[1]][tochka[0]]=figs[figura]

cold=0.9
warm=1.1
hot=1.15
king_m=0.9999

mult=[[1,cold,cold,1,1,cold,cold,1],
      [cold,warm,1,1,1,1,warm,cold],
      [cold,warm,hot,hot,hot,hot,warm,cold],
      [cold,1,hot,hot,hot,hot,1,cold],
      [cold,1,hot,hot,hot,hot,1,cold],
      [cold,warm,hot,hot,hot,hot,warm,cold],
      [cold,warm,1,1,1,1,warm,cold],
      [1,cold,cold,1,1,cold,cold,1]]

king_mult=[[1,1,1,1,1,1,1,1],
           [king_m,king_m,king_m,king_m,king_m,king_m,king_m,king_m],
           [king_m,king_m,king_m,king_m,king_m,king_m,king_m,king_m],
           [king_m,king_m,king_m,king_m,king_m,king_m,king_m,king_m],
           [king_m,king_m,king_m,king_m,king_m,king_m,king_m,king_m],
           [king_m,king_m,king_m,king_m,king_m,king_m,king_m,king_m],
           [king_m,king_m,king_m,king_m,king_m,king_m,king_m,king_m],
           [1,1,1,1,1,1,1,1]]

def podstanovka(ax: int, ay: int, dx: int, dy: int, hod: int) -> float:
    global bel, bla
    if hod%2:
        if doska[ay][ax]!=figs[6] and doska[ay][ax]!=figs[7]: bla+=cost[figs.index(doska[ay][ax])]*(mult[ay+dy][ax+dx]-mult[ay][ax])
        elif doska[ay][ax]==figs[6]: bla+=10_000*(king_mult[ay+dy][ax+dx]-king_mult[ay][ax])
        bel-=cost[figs.index(doska[ay+dy][ax+dx])]*mult[ay+dy][ax+dx]
    else:
        if doska[ay][ax]!=figs[0] and doska[ay][ax]!=figs[1]: bel+=cost[figs.index(doska[ay][ax])]*(mult[ay+dy][ax+dx]-mult[ay][ax])
        elif doska[ay][ax]==figs[0]: bel+=10_000*(king_mult[ay+dy][ax+dx]-king_mult[ay][ax])
        bla-=cost[figs.index(doska[ay+dy][ax+dx])]*mult[ay+dy][ax+dx]
    last=doska[ay+dy][ax+dx]
    doska[ay+dy][ax+dx]=doska[ay][ax]
    doska[ay][ax]=" "
    itog=bot(hod)
    doska[ay][ax]=doska[ay+dy][ax+dx]
    doska[ay+dy][ax+dx]=last
    if hod%2:
        if doska[ay][ax]!=figs[6] and doska[ay][ax]!=figs[7]: bla-=cost[figs.index(doska[ay][ax])]*(mult[ay+dy][ax+dx]-mult[ay][ax])
        elif doska[ay][ax]==figs[6]: bla-=10_000*(king_mult[ay+dy][ax+dx]-king_mult[ay][ax])
        bel+=cost[figs.index(doska[ay+dy][ax+dx])]*mult[ay+dy][ax+dx]
    else:
        if doska[ay][ax]!=figs[0] and doska[ay][ax]!=figs[1]: bel-=cost[figs.index(doska[ay][ax])]*(mult[ay+dy][ax+dx]-mult[ay][ax])
        elif doska[ay][ax]==figs[0]: bel-=10_000*(king_mult[ay+dy][ax+dx]-king_mult[ay][ax])
        bla+=cost[figs.index(doska[ay+dy][ax+dx])]*mult[ay+dy][ax+dx]
    bel=round(bel,2)
    bla=round(bla,2)
    return itog
    

def bot(hod: int) -> tuple: #dfs
    global bel, bla, counter
    if not hod:
        counter+=1
        if bel<=0: return 10_000
        if bla<=0: return -10_000
        return bla/bel
    mn=2147483647
    mx=-2147483647
    for y in range(8):
        for x in range(8):
            if hod%2:
                if doska[y][x]==figs[0]:
                    for y1 in range(-1,2):
                        if 8>(y+y1)>-1:
                            for x1 in range(-1,2):
                                if 8>(x+x1)>-1 and (x1 or y1) and doska[y+y1][x+x1] not in figs[:6]:
                                    skolko=podstanovka(x,y,x1,y1,hod-1)
                                    if skolko<mn:
                                        mn=skolko

                elif doska[y][x]==figs[1]:
                    for y1 in range(-1,2):
                        for x1 in range(-1,2):
                            for dal in range(1,8):
                                if 8>(x+x1*dal)>-1 and 8>(y+y1*dal)>-1 and (x1 or y1) and doska[y+y1*dal][x+x1*dal] not in figs[:6] and (dal==1 or doska[y+y1*(dal-1)][x+x1*(dal-1)]==" "):
                                    skolko=podstanovka(x,y,x1*dal,y1*dal,hod-1)
                                    if skolko<mn:
                                        mn=skolko
                                else: break
                                
                elif doska[y][x]==figs[2]:
                    for y1 in range(-1,2):
                        for x1 in range(-1,2):
                            for dal in range(1,8):
                                if 8>(x+x1*dal)>-1 and 8>(y+y1*dal)>-1 and (abs(x1)+abs(y1)==1) and doska[y+y1*dal][x+x1*dal] not in figs[:6] and (dal==1 or doska[y+y1*(dal-1)][x+x1*(dal-1)]==" "):
                                    skolko=podstanovka(x,y,x1*dal,y1*dal,hod-1)
                                    if skolko<mn:
                                        mn=skolko
                                else: break

                elif doska[y][x]==figs[3]:
                    for y1 in range(-1,2):
                        for x1 in range(-1,2):
                            for dal in range(1,8):
                                if 8>(x+x1*dal)>-1 and 8>(y+y1*dal)>-1 and (abs(x1)+abs(y1)==2) and doska[y+y1*dal][x+x1*dal] not in figs[:6] and (dal==1 or doska[y+y1*(dal-1)][x+x1*(dal-1)]==" "):
                                    skolko=podstanovka(x,y,x1*dal,y1*dal,hod-1)
                                    if skolko<mn:
                                        mn=skolko
                                else: break
                                        
                elif doska[y][x]==figs[4]:
                    for x1,y1 in ((-1,-2),(-2,-1),(-1,2),(2,-1),(1,-2),(-2,1),(1,2),(2,1)):
                        if -1<(x+x1)<8 and -1<(y+y1)<8 and doska[y+y1][x+x1] not in figs[:6]:
                            skolko=podstanovka(x,y,x1,y1,hod-1)
                            if skolko<mn:
                                mn=skolko
                                
                elif doska[y][x]==figs[5]:
                    hody=[]
                    if doska[y-1][x]==" ": hody.append((0,-1))
                    if y==1 and doska[y-1][x]==" " and doska[y-2][x]==" ": hody.append((0,-2))
                    if x<7 and doska[y-1][x+1] in figs[6:12]: hody.append((1,-1))
                    if x>0 and doska[y-1][x-1] in figs[6:12]: hody.append((-1,-1))
                    if (y!=1):
                        for (x1,y1) in hody:
                            skolko=podstanovka(x,y,x1,y1,hod-1)
                            if skolko<mn:
                                mn=skolko
                                
                    else:
                        for perekvalifikaciya in (figs[4],figs[1]):
                            doska[y][x]=perekvalifikaciya
                            if perekvalifikaciya==figs[4]: bel+=2*mult[y][x]
                            else: bel+=9-mult[y][x]
                            for (x1,y1) in hody:
                                skolko=podstanovka(x,y,x1,y1,hod-1)
                                if skolko<mn:
                                    mn=skolko
                            if perekvalifikaciya==figs[4]: bel-=2*mult[y][x]
                            else: bel-=9-mult[y][x]
                            doska[y][x]=figs[5]

            else:
                if doska[y][x]==figs[6]:
                    for y1 in range(-1,2):
                        if 8>(y+y1)>-1:
                            for x1 in range(-1,2):
                                if 8>(x+x1)>-1 and (x1 or y1) and doska[y+y1][x+x1] not in figs[6:12]:
                                    skolko=podstanovka(x,y,x1,y1,hod-1)
                                    if skolko>mx:
                                        
                                        mx=skolko
                                        if hod==4: tot=(x,y,x1,y1)

                elif doska[y][x]==figs[7]:
                    for y1 in range(-1,2):
                        for x1 in range(-1,2):
                            for dal in range(1,8):
                                if 8>(x+x1*dal)>-1 and 8>(y+y1*dal)>-1 and (x1 or y1) and doska[y+y1*dal][x+x1*dal] not in figs[6:12] and (dal==1 or doska[y+y1*(dal-1)][x+x1*(dal-1)]==" "):
                                    skolko=podstanovka(x,y,x1*dal,y1*dal,hod-1)
                                    if skolko>mx:
                                        mx=skolko
                                        if hod==4: tot=(x,y,x1,y1)
                                else: break
                                        
                elif doska[y][x]==figs[8]:
                    for y1 in range(-1,2):
                        for x1 in range(-1,2):
                            for dal in range(1,8):
                                if 8>(x+x1*dal)>-1 and 8>(y+y1*dal)>-1 and (abs(x1)+abs(y1)==1) and doska[y+y1*dal][x+x1*dal] not in figs[6:12] and (dal==1 or doska[y+y1*(dal-1)][x+x1*(dal-1)]==" "):
                                    skolko=podstanovka(x,y,x1*dal,y1*dal,hod-1)
                                    if skolko>mx:
                                        mx=skolko
                                        if hod==4: tot=(x,y,x1,y1)
                                else: break

                elif doska[y][x]==figs[9]:
                    for y1 in range(-1,2):
                        for x1 in range(-1,2):
                            for dal in range(1,8):
                                if 8>(x+x1*dal)>-1 and 8>(y+y1*dal)>-1 and (abs(x1)+abs(y1)==2) and doska[y+y1*dal][x+x1*dal] not in figs[6:12] and (dal==1 and doska[y+y1*(dal-1)][x+x1*(dal-1)]==" "):
                                    skolko=podstanovka(x,y,x1*dal,y1*dal,hod-1)
                                    if skolko>mx:
                                        mx=skolko
                                        if hod==4: tot=(x,y,x1,y1)
                                else: break

                elif doska[y][x]==figs[10]:
                    for x1,y1 in ((-1,-2),(-2,-1),(-1,2),(2,-1),(1,-2),(-2,1),(1,2),(2,1)):
                        if -1<(x+x1)<8 and -1<(y+y1)<8 and doska[y+y1][x+x1] not in figs[6:12]:
                            skolko=podstanovka(x,y,x1,y1,hod-1)
                            if skolko>mx:
                                mx=skolko
                                if hod==4: tot=(x,y,x1,y1)

                elif doska[y][x]==figs[11]:
                    hody=[]
                    if doska[y+1][x]==" ":
                        hody.append((0,1))
                    if y==1 and doska[y+1][x]==" " and doska[y+2][x]==" ": hody.append((0,2))
                    if x<7 and doska[y+1][x+1] in figs[:6]: hody.append((1,1))
                    if x>0 and doska[y+1][x-1] in figs[:6]: hody.append((-1,1))
                    if (y!=6):
                        for (x1,y1) in hody:
                            skolko=podstanovka(x,y,x1,y1,hod-1)
                            if skolko>mx:
                                mx=skolko
                                if hod==4: tot=(x,y,x1,y1)
                    else:
                        for perekvalifikaciya in (figs[10],figs[7]):
                            doska[y][x]=perekvalifikaciya
                            if perekvalifikaciya==figs[10]: bla+=2*mult[y][x]
                            else: bla+=9-mult[y][x]
                            for (x1,y1) in hody:
                                skolko=podstanovka(x,y,x1,y1,hod-1)
                                if skolko>mx:
                                    
                                    mx=skolko
                                    if hod==4: tot=(x,y,x1,y1, perekvalifikaciya)
                            if perekvalifikaciya==figs[10]: bla-=2*mult[y][x]
                            else: bla-=(9-mult[y][x])
                            doska[y][x]=figs[11]
                    
    if hod!=4:
        if hod%2:
            return mn
        return mx
    print(tot,"\nmx =",mx)
    return tot



def scan(ot: tuple, kuda: tuple) -> bool:
    raznx=kuda[0]-ot[0]
    razny=kuda[1]-ot[1]
    try: znx=raznx//abs(raznx)
    except:
        zny=razny//abs(razny)
        for prov in range(ot[1]+zny, kuda[1],zny):
            if doska[prov][kuda[0]]!=" ": return False
        return True
    try: zny=razny//abs(razny)
    except:
        znx=raznx//abs(raznx)
        for prov in range(ot[0]+znx, kuda[0],znx):
            if doska[kuda[1]][prov]!=" ": return False
        return True
    for prov in range(1,abs(raznx)):
        if doska[ot[1]+prov*zny][ot[0]+prov*znx]!=" ": return False
    return True


def view() -> None:
    global bel, bla
    bel=round(bel,2)
    bla=round(bla,2)
    print(bel,bla,sep=(18-len(str(bel))-len(str(bla)))*" ")
    for y in range(8):
        print(8-y, end=" ")
        for x in range(8):
            if ((x+y)%2): print(f"{black_bg}{doska[y][x]}", end=f" {reset}")
            else: print(f"{white_bg}{doska[y][x]}", end=f" {reset}")
        print()
    print("  A B C D E F G H")


def hod() -> tuple:
    try:
        ent=input("Ход: ").lower()
        ent=ent[:2]+" "+ent[2:]
        fr,to=ent.split()
        fr=(ord(fr[0])-97, 8-int(fr[1]))
        to=(ord(to[0])-97, 8-int(to[1]))
    except:
        print(red_bg+"Введи нормально"+reset)
        return ()
    print(fr,to)
    if fr==to: print(red_bg+"Себя есть нельзя. Очень нельзя"+reset)
    elif to[0]>7 or to[0]<0 or to[1]>7 or to[1]<0: print(red_bg+"Давай только по полю бегать"+reset)
    elif doska[to[1]][to[0]] in figs[:6]: print(red_bg+"Своих есть нельзя. Они обидятся"+reset)
    # dfs
    elif doska[fr[1]][fr[0]] in figs[1:4] and not scan(fr,to): print(red_bg+"Куда полетел?"+reset)
    elif doska[fr[1]][fr[0]]==figs[0]:
        if abs(to[0]-fr[0])>1 or abs(to[1]-fr[1])>1: print(red_bg+"Ты так не можешь прыгать королем"+reset)
        else: return (fr,to)
    elif doska[fr[1]][fr[0]]==figs[1]:
        if to[0]-fr[0] and to[1]-fr[1] and abs(to[0]-fr[0])!=abs(to[1]-fr[1]): print(red_bg+"У тебя было много вариантов сходить... но ты не нашел ни одного"+reset)
        else: return (fr,to)
    elif doska[fr[1]][fr[0]]==figs[2]:
        if to[0]-fr[0] and to[1]-fr[1]: print(red_bg+"Двигайся по прямым. Это несложно (как я думаю)"+reset)
        else: return (fr,to)
    elif doska[fr[1]][fr[0]]==figs[3]:
        if abs(to[0]-fr[0])!=abs(to[1]-fr[1]): print(red_bg+"Двигайся по диагонали"+reset)
        else: return (fr,to)
    elif doska[fr[1]][fr[0]]==figs[4]:
        if max(abs(to[0]-fr[0]),abs(to[1]-fr[1]))!=2 or min(abs(to[0]-fr[0]),abs(to[1]-fr[1]))!=1: print(red_bg+"Ходи бугвой Г"+reset)
        else: return (fr,to)
    elif doska[fr[1]][fr[0]]==figs[5]:
        if fr[1]-to[1]==1 and (doska[to[1]][to[0]]==" " and not (to[0]-fr[0]) or doska[to[1]][to[0]]!=" " and abs(to[0]-fr[0])==1) or fr[1]-to[1]==2 and fr[1]==6 and doska[to[1]+1][to[0]]==" " and doska[to[1]][to[0]]==" ":
            return (fr,to)
        else: print(red_bg+"Нельзя так пешкой ходить. Подумай снова"+reset)
    else: print(red_bg+"Неправильная команда. Пиши снова"+reset)
    return ()


bel=-10_000
bla=-10_000
for y in range(8):
    for x in range(8):
        if doska[y][x] in figs[:6]: bel+=cost[figs.index(doska[y][x])]*mult[y][x]
        elif doska[y][x] in figs[6:12]: bla+=cost[figs.index(doska[y][x])]*mult[y][x]

import time
vr=0

while bel>0 and bla>0:
    view()
    ans=hod()
    if not len(ans): continue
    if doska[ans[0][1]][ans[0][0]]!=black_txt+"♔": bel+=cost[figs.index(doska[ans[0][1]][ans[0][0]])]*(mult[ans[1][1]][ans[1][0]]-mult[ans[0][1]][ans[0][0]])
    else: bel+=cost[figs.index(doska[ans[0][1]][ans[0][0]])]*(king_mult[ans[1][1]][ans[1][0]]-king_mult[ans[0][1]][ans[0][0]])
    bla-=cost[figs.index(doska[ans[1][1]][ans[1][0]])]*mult[ans[1][1]][ans[1][0]]
    if (doska[ans[0][1]][ans[0][0]]==figs[5]) and ans[0][1]==1:
        doska[ans[1][1]][ans[1][0]]=white_txt+"♕♖♗♘"[int(input("Какую фигурку хошь?\n1 - Ферзь\n2 - Ладья\n3 - Слон\n4 - Поник"))-1]
        if doska[ans[1][1]][ans[1][0]] != figs[1]: bel+=cost[figs.index(doska[ans[1][1]][ans[1][0]])]*mult[ans[1][1]][ans[1][0]]-mult[ans[0][1]][ans[0][0]]
        else: bel+=9-mult[ans[0][1]][ans[0][0]]
    else: doska[ans[1][1]][ans[1][0]]=doska[ans[0][1]][ans[0][0]]
    doska[ans[0][1]][ans[0][0]]=" "
    view()
    counter=0
    timer=time.time()
    geniy=bot(4)
    vr+=time.time()-timer
    print("{} сек\n{:,} вариантов ходов".format(vr, counter))
    if doska[geniy[1]][geniy[0]]!=figs[6]: bla+=cost[figs.index(doska[geniy[1]][geniy[0]])]*(mult[geniy[1]+geniy[3]][geniy[0]+geniy[2]]-mult[geniy[1]][geniy[0]])
    else: bla+=cost[figs.index(doska[geniy[1]][geniy[0]])]*(king_mult[geniy[1]+geniy[3]][geniy[0]+geniy[2]]-king_mult[geniy[1]][geniy[0]])
    bel-=cost[figs.index(doska[geniy[1]+geniy[3]][geniy[0]+geniy[2]])]*mult[geniy[1]+geniy[3]][geniy[0]+geniy[2]]
    if len(geniy)==5:
        doska[geniy[1]+geniy[3]][geniy[0]+geniy[2]]=geniy[4]
        if geniy[4]==figs[10]: bla+=3*mult[geniy[1]+geniy[3]][geniy[0]+geniy[2]]-mult[geniy[1]][geniy[0]]
        else: bla+=9-mult[geniy[1]][geniy[0]]
    else: doska[geniy[1]+geniy[3]][geniy[0]+geniy[2]]=doska[geniy[1]][geniy[0]]
    doska[geniy[1]][geniy[0]]=" "
