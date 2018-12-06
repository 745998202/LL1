from copy import deepcopy

def kill_left_back(relize_words):       #消除左递归，返回消除之后整理的函数
    new_relize_words = {}               #用于返回的新的文法集
    for i in relize_words:              #遍历每一个文法
        help_make_new_relize_words = []
        if_not_end_char = True
        not_end_char = ''
        one_trans_result = ''
        for one_char in i:
            if one_char in '->':
                if_not_end_char = False
            elif one_char not in '->':  #不是无用符
                if if_not_end_char:     #如果在终结符之前
                    not_end_char = not_end_char + one_char#则是非终结符
                else:#在终结符之后
                    if len(one_trans_result)!=0 and one_char == '|':
                        help_make_new_relize_words.append(one_trans_result)
                        one_trans_result = ''
                    else:
                        one_trans_result = one_trans_result+one_char
        if len(one_trans_result)!=0:
            help_make_new_relize_words.append(one_trans_result)
            one_trans_result = ''
        new_relize_words[not_end_char] = help_make_new_relize_words
    print('经过改造后的文法规则为：',new_relize_words)
    help_around_not_end_char_list = deepcopy(new_relize_words)
    for i in help_around_not_end_char_list:
        new_state = i[:] +'\''
        if_has_left_back = False                    #判断是否有左递归的标记量
        save_list = []                              #保留在原来文法中的结果式
        other_list = []                             #放置在新的文法中的结果式
        for one_tran_word in new_relize_words[i]:   #对于单个文法的某个结果转换式
            if one_tran_word[0] == i:
                if_has_left_back = True             #将含有左递归的标记量记为True
                other_list.append(one_tran_word[1:])
            else:
                save_list.append(one_tran_word)
        if if_has_left_back:                        #含有左递归式
            new_relize_words[i].clear()
            for add_decorate in range(len(save_list)):
                save_list[add_decorate] = save_list[add_decorate]+new_state
            for add_decorate in range(len(other_list)):
                other_list[add_decorate] = other_list[add_decorate]+new_state
            if len(save_list) == 0:
                new_relize_words[i] = new_state
            else:
                new_relize_words[i] = save_list
            if len(other_list)!=0:
                other_list.append('e')
                new_relize_words[new_state] = other_list

    print('消除左递归之后的文法为：',new_relize_words)
    return new_relize_words
def get_first_list(relize_words):       #获得FIRST集
    if_changed = True                   #终止条件，如果这次没有改变First集合则推出循环
    First = {}
    for i in relize_words:
        First[i] = []
    new_First = {}
    for i in relize_words:
        new_First[i] = []  # 创建新的First集合，继续第二次循环
    print('初始的First集合为:',First)
    end_char_words = []
    for word in relize_words:
        end_char_words.append(word)
    print('所有的非终结符状态为:',end_char_words)
    while if_changed:                   #当上一次改变了的时候
        if_changed = False
        for end_char in relize_words:   #for every char in relize_words , you can use it to over every state
            for word in relize_words[end_char]: # for every state , you can get a list for First(X)
                if word[0] not in end_char_words:#当不是终结符时
                    if word[0] not in new_First[end_char]:
                        new_First[end_char].append(word[0])
                        if_changed = True
                else:
                    for num in range(len(word)):
                        if word[num] not in end_char_words:#如果循环到终结符，就停止循环
                            if word[num] not in new_First[end_char]:
                                new_First[end_char].append(word[num])
                                if_changed = True
                            break
                        if word[num] in end_char_words and 'e' in new_First[word[num]]:#如果是非终结符且这个非终结符的First集合含有空集
                            help_trans_list = new_First[word[num]][:]
                            help_trans_list.remove('e')
                            if word[num] not in new_First[end_char]:#未加入过这个First集合
                                for new_member in help_trans_list:
                                    if new_member not in new_First[end_char]:
                                        new_First[end_char].append(new_member)
                                        if_changed = True
                        elif 'e' not in new_First[word[num]]:
                            help_trans_list = new_First[word[num]][:]
                            if word[num] not in new_First[end_char]:#未加入过这个First集合
                                new_First[end_char] = new_First[end_char] + help_trans_list
                                if_changed = True
                            break
        First = new_First
    print('First集合为===========================#')
    for i,j in First.items():
        print('First(',i,'): ',j)
def get_follow_list(relize_words):
















if __name__ == '__main__':
    relize_num = int(input('请输入你的文法个数'))
    relize_words = []
    for i in range(relize_num):
        print('输入第',i+1,'个文法')
        one_relize_word = input()
        relize_words.append(one_relize_word)
    print('你输入的文法规则为：',relize_words)
    #==================消除左递归====================#
    relize_words = kill_left_back(relize_words)   # relize_words 消除左递归之后的文法
    #==================得到FIRST集===================#
    get_first_list(relize_words)
    #==================得到FOLLOW集==================#

    #==================生成预分析表格================#

