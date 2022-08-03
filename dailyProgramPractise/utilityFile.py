class Utility:
    def fizubzz(self,num):
        for i in range(1, num + 1):
            if i % 3 == 0 and i % 5 == 0:
                print(i, 'FizzBuzz')
            elif i % 3 == 0 and i % 5 != 0:
                print(i, 'Fizz')
            elif i % 3 != 0 and i % 5 == 0:
                print(i, 'Buzz')
            else:
                print(i)

    def is_palindrome(self,str_val):
        if len(str_val) == 1:
            return True
        else:
            str_val=str_val.lower()
            for i in range(int(len(str_val) // 2)):
                if str_val[i] != str_val[len(str_val) - i - 1]:
                    return False

            return True

    def return_fibonacci(self,num):
        if num==0:
            return False
        elif num==1:
            print(0)
        else:
            a=0
            b=1
            count=0
            while count < num:
                print(a)
                nth =a+b
                a = b
                b = nth
                count+=1

    def merge_array(self,list_1,list_2):
        temp_list=list_1.copy()
        temp_list.extend(list_2)
        print(temp_list)

    def sort_array(self,list_1):
        for i in range(len(list_1)):
            for j in range(i):
                if list_1[i]<list_1[j]:
                    list_1[i],list_1[j]=list_1[j],list_1[i]
        return list_1
def binary_search(list_1,val):
    mid = len(list_1) // 2

    if len(list_1)//2 < 1:
        if list_1[0]==val:
            print('Found')
        else:
            print('Not found')
    else:
        # mid = len(list_1)//2
        if list_1[mid] == val:
            print(list_1[mid],'found')
        elif list_1[mid]>val:
            binary_search(list_1[:mid],val)
        else:
            binary_search(list_1[mid:],val)

a = Utility()
# a.fizubzz(15)
# print(a.is_palindrome('Able was I ere I saw Elba'))
# print(Utility.is_palindrome("Able was I ere I saw Elba"))
# a.return_fibonacci(2)
# a.merge_array([1,2,3,4],[5,6,7,8,9])

binary_search([1,2,3,4,5,6,7,8],11)
