import tkinter as tk
from tkinter import filedialog
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm
import pgpy
import zlib

window=tk.Tk()
window.title('PGP')
#window.iconbitmap('timg.jpg')
window.geometry('800x500')
#下面三个记录了被加密、解密和压缩文件的次序，暂且用来被当作加解密文件的文件名的区分，后续想想怎么存储一个被加密和被解密后的文件的名字
secrectedFileNum=0
decrptedFileNum=0
compressedFileNum=0
decompressedFileNum=0
#存储密钥信息（如昵称、邮箱）的列表
secrectNickNameContent=[]
secrectEmailNmaeContent=[]
secrectNum=0
secrectListPublicFileName=''#被选中的公钥的文件名
secrectListPrivateFileName=''#被选中的私钥的文件名
file_path=''#被选中的要进行加密的文件路径
#菜单栏设置
menubar=tk.Menu(window)
#文件菜单栏设置
filemenu=tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='文件',menu=filemenu)
filemenu.add_command(label='新建')
filemenu.add_command(label='打开')
filemenu.add_command(label='保存')
filemenu.add_command(label='退出',command=window.quit())
#编辑菜单栏设置
editMenu=tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='编辑',menu=editMenu)
editMenu.add_command(label='剪切')
editMenu.add_command(label='复制')
editMenu.add_command(label='粘贴')
#帮助菜单栏设置
helpMenu=tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='帮助',menu=helpMenu)
helpMenu.add_command(label='联系开发人员')
#创建三级菜单
submenu = tk.Menu(filemenu)  # 和上面定义菜单一样，不过此处实在File上创建一个空的菜单
filemenu.add_cascade(label='导入', menu=submenu, underline=0)  # 给放入的菜单submenu命名为Import
# 第9步，创建第三级菜单命令，即菜单项里面的菜单项里面的菜单命令（有点拗口，笑~~~）
submenu.add_command(label='Submenu_1')  # 这里和上面创建原理也一样，在Import菜单项中加入一个小菜单命令Submenu_1
# 创建菜单栏完成后，配置让菜单栏menubar显示出来
window.config(menu=menubar)
#左边菜单栏的具体展开即其触发事件
#界面切换管理的具体界面
manageFrame=tk.Frame(window,height=500,width=700)
#文件加密界面

#h=tk.Label(manageFrame, text='on the frame_l1', bg='green')
#创建新密钥时所产生的新的对话框，要求用户输入昵称、邮件等
def newDial():
    def closeWin():
        #实现弹出的创建框的关闭
        secrectNickNameContent.append(nickName.get())
        secrectEmailNmaeContent.append(email.get())
        global secrectNum
        secrectNum+=1
        for i in range(secrectNum-1,secrectNum):
            secretListContent.insert(tk.END, "Email:"+"  "+secrectEmailNmaeContent[i]+"                                                                 "+"NickName:"+"  "+secrectNickNameContent[i])
        #创建私钥、公钥
        # we can start by generating a primary key. For this example, we'll use RSA, but it could be DSA or ECDSA as well
        key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)

        # we now have some key material, but our new key doesn't have a user ID yet, and therefore is not yet usable!
        uid = pgpy.PGPUID.new(nickName.get(), comment='Honest Abe', email=email.get())
        # now we must add the new user id to the key. We'll need to specify all of our preferences at this point
        # because PGPy doesn't have any built-in key preference defaults at this time
        # this example is similar to GnuPG 2.1.x defaults, with no expiration or preferred keyserver
        key.add_uid(uid, usage={KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage},
                    hashes=[HashAlgorithm.SHA256, HashAlgorithm.SHA384, HashAlgorithm.SHA512, HashAlgorithm.SHA224],
                    ciphers=[SymmetricKeyAlgorithm.AES256, SymmetricKeyAlgorithm.AES192, SymmetricKeyAlgorithm.AES128],
                    compression=[CompressionAlgorithm.ZLIB, CompressionAlgorithm.BZ2, CompressionAlgorithm.ZIP,
                                 CompressionAlgorithm.Uncompressed])
        #对私钥进行口令加密
        key.protect(str(passWord.get()), SymmetricKeyAlgorithm.AES256, HashAlgorithm.SHA256)
        #已创建私钥、公钥，现准备将其写入文件中
        pubkey = key.pubkey
        privateFileName=nickName.get()+" "+email.get()+" "+'privateKey'
        publicFileName=nickName.get()+' '+email.get()+' '+'publicKey'
        prikeyFile = open(privateFileName, 'w')
        prikeyFile.write(str(key))
        prikeyFile.close()
        pubkeyFile = open(publicFileName, 'w')
        pubkeyFile.write(str(pubkey))
        pubkeyFile.close()


        #print(nickName.get())#获取输入框里的内容
       # print(email.get())#获取输入框里的内容
        DialWin.destroy()
    DialWin=tk.Tk()
    DialWin.title('CreatSercet')
    DialWin.geometry('400x300')
    vNickName=tk.StringVar()
    vEmail=tk.StringVar()
    vPassWord=tk.StringVar()
    tk.Label(DialWin,text='创建你自己的密钥',fg='black',font=('宋体',22),width=25,height=2).place(x=0,y=20)
    tk.Label(DialWin, text='昵称', fg='black', font=('宋体', 12), width=10, height=2).place(x=50, y=82)
    tk.Label(DialWin, text='邮箱', fg='black', font=('宋体', 12), width=10, height=2).place(x=50, y=132)
    tk.Label(DialWin,text='口令',fg='black',font=('宋体',12),width=10,height=2).place(x=50,y=182)
    nickName=tk.Entry(DialWin,textvariable=vNickName)
    email=tk.Entry(DialWin,textvariable=vEmail)
    passWord=tk.Entry(DialWin,textvariable=vPassWord)
    nickName.place(x=150,y=90)
    email.place(x=150,y=140)
    passWord.place(x=150,y=190)
    tk.Button(DialWin,text="创建",font=('宋体',14),width=8,height=2,command=closeWin).place(x=150,y=240)
    DialWin.mainloop()


#密钥管理界面控件的判断属性
on_hit=False
#加密文件界面控件的判断属性
on_hit1=False
#解密文件界面控件的判断属性
on_hit2=False
#压缩文件界面控件的判断属性
on_hit3=False
#解压文件界面控件的判断属性
on_hit4=False


#创建密钥按钮
miyaoCreatButton=tk.Button(manageFrame,text="创建密钥",font=('宋体',14),width=8,height=2,command=newDial)
#密钥选择列表的相关选项
#创建密钥选择列表
def triggerOnLS(event):#鼠标键盘之类的触发事件；event要注意，否则报错
    #对已经选择的密钥名进行处理，因为我在这里双击获取的密钥名的格式如下所示：Email:  1大赛爱的                                                                 NickName:  撒地方
    secrectListSelected=secretListContent.get(secretListContent.curselection())
    secrectListDealed=secrectListSelected.split('  ')
    global secrectListPublicFileName
    global secrectListPrivateFileName
    secrectListPublicFileName=secrectListDealed[34]+' '+secrectListDealed[1]+" "+'publicKey'#获取了被选中的公钥的文件名
    secrectListPrivateFileName=secrectListDealed[34]+' '+secrectListDealed[1]+' '+'privateKey'#获取了被选中的私钥的文件名
    print(secrectListPublicFileName)
    print(secrectListPrivateFileName)
    #print(secrectListDealed[1])#获取了列表中被选中的密钥的Email名
    #print(secrectListDealed[34])#获取了列表中被选中的密钥的NickName的名字
    print(secretListContent.get(secretListContent.curselection()))
secretListContent=tk.Listbox(manageFrame,width=100,height=15)
secretListContent.bind('<Double-Button-1>',triggerOnLS)#获取键盘的命令后，执行相关的函数
#删除密钥按钮
miyaoDeleteButton=tk.Button(manageFrame,text="删除密钥",font=('宋体',14),width=8,height=2)
#备份密钥按钮
miyaoProtestButton=tk.Button(manageFrame,text="备份密钥",font=('宋体',14),width=8,height=2)






#选择文件按钮的监听函数
#选择的文件的绝对路径名的变量
fileName=tk.StringVar()#相当于一个对象类型啦
#在进行文件解密时获取输入的口令内容
passWordContent=tk.StringVar()
def selectFile():
    global file_path
    file_path=filedialog.askopenfilename()
    fileName.set(file_path)
#选择文件的按钮
fileChosenButton=tk.Button(manageFrame,text='选择文件',font=('宋体',10),width=6,height=1,command=selectFile)
#选择文件后文件路径名的显示框
fileNameEntry=tk.Entry(manageFrame,textvariable=fileName,width=30)
#输入解密时的口令
passWordEntry=tk.Entry(manageFrame,textvariable=passWordContent,width=30)
#确定加密密钥的按钮
fileSecrectQuerenButton=tk.Button(manageFrame,text='选择公钥',font=('宋体',10),width=6,height=1)
#确定解密密钥的按钮
fileDecrptQuerenButton=tk.Button(manageFrame,text='选择私钥',font=('宋体',10),width=6,height=1)
#标题“输入口令”
passWordLabel=tk.Label(manageFrame,text='输入口令',fg='black',font=('宋体',10),width=6,height=1)
#加密文件函数,对‘进行加密’这个按钮的监听按钮
def secrectFile():
    global secrectedFileNum
    secrectedFileNum+=1
    secrectPubKey,_=pgpy.PGPKey.from_file(secrectListPublicFileName)
    #要加密的文件的内容
    file_object = open(file_path)
    all_the_text = file_object.read()
    msg = pgpy.PGPMessage.new(all_the_text)
    #利用已选中的公钥对文件进行加密
    enc_msg = secrectPubKey.encrypt(msg)
    #将文件内容写到新文件中
    dealedFile_path=file_path.split('.')
    new_file_path='D:/PGPSecrectedFile/secrectedFile'+str(secrectedFileNum)+'.'+str(dealedFile_path[1])
    new_file_object=open(new_file_path,'w')
    new_file_object.write(str(enc_msg))
    new_file_object.close()
    print('文件加密成功')
    #print(enc_msg)#打印加密后的文件内容
#对选中的文件进行解密的具体函数实现/对“进行解密”这个按钮的监听函数
def decrptSelectedFile():
    passWordFans=passWordEntry.get()
    global decrptedFileNum
    decrptedFileNum+=1
    secrectPriKey,_=pgpy.PGPKey.from_file(secrectListPrivateFileName)
    #对输入的口令进行判断，利用try...catch块进行
    try:
      with secrectPriKey.unlock(passWordFans):
        # 要解密的文件的内容的读写
        file_object = open(file_path)
        all_the_txt = file_object.read()
        # 从文件中读取了str类型的内容后，要对该内容进行解密需要采用以下方法，及先将已有的内容转为PGPMessage类型，注意采用的是from_blob而不是new
        beingDecrpted = pgpy.PGPMessage.from_blob(all_the_txt)
        # 利用已选中的私钥对文件进行解密
        dec_msg = secrectPriKey.decrypt(beingDecrpted)
        # 下面将解密后的文件内容生成一个新的文件，写在一个新的文件夹里
        dealedFile_path = file_path.split('.')
        new_file_path = 'D:/PGPDecrptedFile/decrptedFile' + str(decrptedFileNum) + '.' + str(dealedFile_path[1])
        new_file_object = open(new_file_path, 'w')
        new_file_object.write(str(dec_msg.message))
        new_file_object.close()
        print('文件解密成功')
    except:
        print("您输入的口令不对！")


    #print(dec_msg.message)
#文件压缩的内部实现函数
def compressFile():
    global compressedFileNum
    compressedFileNum+=1
    file_object=open(file_path,'rb')#rb表示要读写二进制文件，否则会报错：提示不能是str类型，要为bytes类型
    all_the_txt=file_object.read()
    compressedContent=zlib.compress(all_the_txt)
    file_object.close()
    #下面将压缩后的文件内容写入一个新文件中
    new_file_path='D:/PGPCompressFile/compressedFile'+str(compressedFileNum)+'.'+'txt'
    new_file_object=open(new_file_path,'wb')
    new_file_object.write(compressedContent)
    new_file_object.close()
    print('文件压缩成功')
#文件解压缩的内部实现函数
def decompressFile():
    global decompressedFileNum
    decompressedFileNum+=1
    file_object=open(file_path,'rb')
    all_the_txt=file_object.read()
    decompressedContent=zlib.decompress(all_the_txt)
    file_object.close()
    # 下面将解压缩后的文件内容写入一个新文件中
    new_file_path = 'D:/PGPDecompressedFile/decompressedFile' + str(decompressedFileNum) + '.' + 'txt'
    new_file_object = open(new_file_path, 'wb')
    new_file_object.write(decompressedContent)
    new_file_object.close()
    print('文件解压缩成功')


#确定要进行加密的按钮
sureToSecrectButton=tk.Button(manageFrame,text='进行加密',font=('宋体',10),width=6,height=1,command=secrectFile)
#确定要进行解密的按钮
sureToDecrptButton=tk.Button(manageFrame,text='进行解密',font=('宋体',10),width=6,height=1,command=decrptSelectedFile)
#确定要进行文件压缩的按钮
sureToCompressButton=tk.Button(manageFrame,text='进行压缩',font=('宋体',10),width=6,height=1,command=compressFile)
#确定要进行文件解压缩的按钮
sureToDecompressButton=tk.Button(manageFrame,text='解压缩',font=('宋体',10),width=6,height=1,command=decompressFile)


#欢迎标语
tk.Label(manageFrame,text='欢迎使用PGPTools',fg='black',font=('宋体',14),width=25,height=2).place(x=240,y=0)

manageFrame.pack()
#压缩文件的界面
def compressionFileUI():
    global on_hit3
    if on_hit3==False:
        on_hit3=True
        fileChosenButton.place(x=450,y=200,anchor='nw')
        sureToCompressButton.place(x=600,y=200,anchor='nw')
        fileNameEntry.place(x=130,y=200,anchor='nw')
    else:
        on_hit3=False
        fileChosenButton.place_forget()
        sureToCompressButton.place_forget()
        fileNameEntry.place_forget()
#解压缩文件的界面
def decompressFileUI():
    global on_hit4
    if on_hit4==False:
        on_hit4=True
        fileChosenButton.place(x=450, y=200, anchor='nw')
        sureToDecompressButton.place(x=600, y=200, anchor='nw')
        fileNameEntry.place(x=130, y=200, anchor='nw')
    else:
        on_hit4=False
        fileChosenButton.place_forget()
        sureToDecompressButton.place_forget()
        fileNameEntry.place_forget()



#解密文件的界面
def decrptFile():
    global on_hit2
    if on_hit2==False:
        on_hit2=True
        fileChosenButton.place(x=370, y=400, anchor='nw')
        fileDecrptQuerenButton.place(x=450, y=400, anchor='nw')
        passWordLabel.place(x=130,y=440,anchor='nw')
        passWordEntry.place(x=190,y=440,anchor='nw')
        fileNameEntry.place(x=130, y=400, anchor='nw')
        sureToDecrptButton.place(x=520, y=400, anchor='nw')
        secretListContent.place(x=100, y=50, anchor='nw')
    else:
        on_hit2 = False
        fileDecrptQuerenButton.place_forget()
        sureToDecrptButton.place_forget()
        passWordLabel.place_forget()
        passWordEntry.place_forget()
        fileChosenButton.place_forget()
        secretListContent.place_forget()
        fileNameEntry.place_forget()

#加密文件的界面
def secrectFile():
    global on_hit1
    if on_hit1==False:
        on_hit1=True
        fileChosenButton.place(x=370,y=400,anchor='nw')
        fileSecrectQuerenButton.place(x=450,y=400,anchor='nw')
        fileNameEntry.place(x=130,y=400,anchor='nw')
        sureToSecrectButton.place(x=520,y=400,anchor='nw')
        secretListContent.place(x=100, y=50, anchor='nw')
    else:
        on_hit1=False
        fileSecrectQuerenButton.place_forget()
        sureToSecrectButton.place_forget()
        fileChosenButton.place_forget()
        secretListContent.place_forget()
        fileNameEntry.place_forget()


#管理密钥的界面
def manage():
    global on_hit
    if on_hit==False:
        on_hit=True
        miyaoCreatButton.place(x=130,y=400,anchor='nw')
        miyaoDeleteButton.place(x=280,y=400,anchor='nw')
        miyaoProtestButton.place(x=430,y=400,anchor='nw')
        secretListContent.place(x=100,y=50,anchor='nw')
    else:
        miyaoCreatButton.place_forget()
        miyaoDeleteButton.place_forget()
        miyaoProtestButton.place_forget()
        secretListContent.place_forget()
        on_hit=False

#加密文件
#界面左端菜单栏
manageButton=tk.Button(window,text='密钥管理',font=('宋体',14),width=8,height=2,command=manage).place(x=0,y=50,anchor='nw')
secretButton=tk.Button(window,text='加密文件',font=('宋体',14),width=8,height=2,command=secrectFile).place(x=0,y=110,anchor='nw',)
decretButton=tk.Button(window,text='解密文件',font=('宋体',14),width=8,height=2,command=decrptFile).place(x=0,y=170,anchor='nw')
zipButton=tk.Button(window,text='文件压缩',font=('宋体',14),width=8,height=2,command=compressionFileUI).place(x=0,y=230,anchor='nw')
unzipButton=tk.Button(window,text='文件解压',font=('宋体',14),width=8,height=2,command=decompressFileUI).place(x=0,y=290,anchor='nw')





window.mainloop()
