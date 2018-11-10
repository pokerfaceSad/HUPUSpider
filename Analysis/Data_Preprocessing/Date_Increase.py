def date_increase(List):
    '''
    Input the Date_List
    Output the Changed_List
    '''
    if List[0] % 400 == 0 and (List[0] % 4 == 0 and List[0] % 100 != 0):  # 是闰年
        if List[1] == 2:
            if List[2] < 29:
                List[2] = List[2] + 1
            else:
                List[2] = 1
                List[1] = List[1] + 1
        elif List[1] in [1, 3, 5, 7, 8, 10, 12]:  # 大月份
            if List[2] < 31:
                List[2] = List[2] + 1
            else:
                List[2] = 1
                if List[1] != 12:
                    List[1] = List[1] + 1  # 月份数加一
                else:
                    List[1] = 1
                    List[0] = List[0] + 1  # 年数加一
        elif List[1] in [4, 6, 9, 11]:
            if List[2] < 30:
                List[2] = List[2] + 1
            else:
                List[2] = 1
                List[1] = List[1] + 1  # 月份数加一
    else:
        if List[1] == 2:
            if List[2] < 28:
                List[2] = List[2] + 1
            else:
                List[2] = 1
                List[1] = List[1] + 1
        elif List[1] in [1, 3, 5, 7, 8, 10, 12]:  # 大月份
            if List[2] < 31:
                List[2] = List[2] + 1
            else:
                List[2] = 1
                if List[1] != 12:
                    List[1] = List[1] + 1  # 月份数加一
                else:
                    List[1] = 1
                    List[0] = List[0] + 1  # 年数加一
        elif List[1] in [4, 6, 9, 11]:
            if List[2] < 30:
                List[2] = List[2] + 1
            else:
                List[2] = 1
                List[1] = List[1] + 1  # 月份数加一
    return List
