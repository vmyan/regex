from pprint import pprint
import re
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
pprint(contacts_list)


def change_name(text):
    new_list = list()
    for item in text:
        full_name = ' '.join(item[0:3]).split(' ')[0:3]
        result = [full_name[0], full_name[1], full_name[2], item[3], item[4], item[5], item[6]]
        new_list.append(result)
    return new_list


def clear_duplicates(correct_list):
    no_duplicates = []
    for item in correct_list:
        for name in correct_list:
            if item[0:2] == name[0:2]:
                list_name = item
                item = list_name[0:2]
                for i in range(2, 7):
                    if list_name[i] == '':
                        item.append(name[i])
                    else:
                        item.append(list_name[i])
        if item not in no_duplicates:
            no_duplicates.append(item)

    return no_duplicates


def change_phone(phone_pattern, changed_pattern, text):
    phonebook = [[re.sub(phone_pattern, changed_pattern, string) for string in strings] for strings in text]
    return phonebook


if __name__ == "__main__":
    correct_list_with_duplicates = change_name(contacts_list)
    clear_list = clear_duplicates(correct_list_with_duplicates)

    pattern_1 = r'+7(\2)\3-\4-\5'
    clear_list = change_phone(r'(\+7|8)*[\s\(]*(\d{3})[\)\s-]*(\d{3})[-]*(\d{2})[-]*(\d{2})[\s\(]',
                              pattern_1, clear_list)
    clear_list = change_phone(r'(\+7|8)(\d{3})(\d{3})(\d{2})(\d{2})', pattern_1, clear_list)
    clear_list = change_phone(r'(\+7|8)\s(\d{3})[-](\d{3})[-](\d{2})(\d{2})', pattern_1, clear_list)
    clear_list = change_phone(r'(\+7|8)\s[(](\d{3})[)]\s(\d{3})[-](\d{2})[-](\d{2})', pattern_1, clear_list)
    changed_phonebook = change_phone(
        r'(\+7|8)+[\s(]*(\d{3,3})[\s)-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})[\s]*[(доб.\s]*(\d+)[)]*',
        r'+7(\2)\3-\4-\5 доб.\6', clear_list)

with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(changed_phonebook)
