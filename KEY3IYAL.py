from random import seed
from random import randint

print("WELCOME TO 3IYAL SECRET MESSAGES")
print('CHOOSE 1 FOR ENCRYPTION OR 2 FOR DECRYPTION MODE')
option=int(input(""))
if option==1:
    decrypted = input("Enter your message bruh")
    print("You have entered : ", decrypted)
    encrypted = []
    key3iyal = []
    for i in decrypted:
        x = randint(0, 255 - ord(i))
        encrypted.append(chr(x + ord(i)))
        key3iyal.append(x)
    print(''.join(encrypted))
    print(' '.join(str(e) for e in key3iyal))
elif option==2:
    encrypted=input("Enter your encrypted message pessiron")
    key3iyal=input("Enter your key")
    key3iyal=key3iyal.split(" ")
    decrypted=[]
    j=0
    for i in encrypted :
        kk=encrypted.find(i,j)
        decrypted.append(chr(ord(i)-int(key3iyal[kk])))
        j=j+1
    print("YOU DECRYPTED MESSAGE IS",''.join(decrypted))
else:
    print("error , please choose a valid option (1 or 2 ya fanen)")
