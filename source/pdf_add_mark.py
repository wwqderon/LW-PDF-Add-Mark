import csv
import re
from PyPDF2 import PdfFileWriter, PdfFileReader




def read_mark_txt(file_path, chapter_name):
    with open(file_path, 'r', encoding='utf-8') as fp:
        parent_list = []
        parent_num_list = []
        section_list = []
        number_list = []
        for line in fp.readlines():
            line = line.replace('.', ' ')
            line_split = line.split()
            if line_split[0] == 'Part':
                continue
            if line_split[0] in [chapter_name] and bool(section_list) is True:
                parent_list.append(section_list)
                parent_num_list.append(number_list)
                section_list = []
                number_list = []

            label = ' '.join(line_split[:-1])
            section_list.append(label)
            number_list.append(line_split[-1])
        parent_list.append(section_list)
        parent_num_list.append(number_list)

    return parent_list, parent_num_list

def read_csv_mark(csv_file):
    csv_open = open(csv_file, 'r', newline='', encoding='gbk')
    mark_csv_reader = csv.reader(csv_open)
    mark_page_number_list = []
    for row in mark_csv_reader:
        while '' in row:
            row.remove('')
        row = row[0:3]
        mark_page_number_list.append(row)
    return mark_page_number_list

def create_pdf_mark(pdf_name, parent_list, parent_num_list, tolerance=0):
    output = PdfFileWriter()
    pdf_reader = PdfFileReader(open(pdf_name, 'rb'))
    pdf_page_number = pdf_reader.getNumPages()
    for i in range(pdf_page_number):
        output.addPage(pdf_reader.getPage(i))
    for i, parent in enumerate(parent_list):
        for j, section in enumerate(parent):
            if j == 0:
                #print(section)
                parent_add = output.addBookmark(section, int(int(parent_num_list[i][j]))+tolerance)
            else:
                #print(parent_add)
                if parent_num_list[i][j].isdigit():
                    output.addBookmark(section, int(parent_num_list[i][j])+tolerance, parent_add)
    # Write to an output PDF document
    output1 = open(pdf_name + '_addmark.pdf', "wb")
    output.write(output1)
    pdf_reader = PdfFileReader(open(pdf_name, 'rb'))


def create_pdf_mark_csv(pdf_name, mark_page_number_list, tolerance=0):
    output = PdfFileWriter()
    pdf_reader = PdfFileReader(open(pdf_name, 'rb'))
    pdf_page_number = pdf_reader.getNumPages()
    for i in range(pdf_page_number):
        output.addPage(pdf_reader.getPage(i))
    for i, elem in enumerate(mark_page_number_list):
        if len(elem) < 2:
            continue
        page_number_level = elem[0]
        page_title = elem[1]
        page_number = elem[2]
        page_number_add = int(int(page_number)+tolerance-2)
        #添加1级目录
        if int(page_number_level) > 3:
            page_number_level = '1'
        if page_number_level == '1':
            #print(section)
            parent_1 = output.addBookmark(page_title, page_number_add)
        # 在1级目录下，添加2级目录
        elif page_number_level == '2' or page_number_level == '':
            parent_2 = output.addBookmark(page_title, page_number_add, parent_1)
        # 在1级目录下，添加3级目录
        elif page_number_level == '3':
            parent_3 = output.addBookmark(page_title, page_number_add, parent_2)
    # Write to an output PDF document
    output_pdf_open = open(pdf_name.split('.')[0] + '_addmark.pdf', "wb")
    output.write(output_pdf_open)
    pdf_reader = PdfFileReader(open(pdf_name, 'rb'))

if __name__ == '__main__':

    #parent_1, parent_num_1 = read_mark_txt('zhengpan.txt', '第')
    #print(parent_1, parent_num_1)
    #create_pdf_mark('曾攀的《有限元分析基础教程》.pdf', parent_1, parent_num_1, 13)
    csv_reader = read_csv_mark('有限元法：理论、格式与求解方法(第2版下)_巴特.csv')
    print(csv_reader)
    create_pdf_mark_csv('有限元法：理论、格式与求解方法(第2版下)_巴特.pdf', csv_reader, 18)