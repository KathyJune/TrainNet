# -*- coding: utf-8 -*-
import xlrd
import xlwt
import node


class TrainMtx:
    def __init__(self, f):
        self.f = f
        self.data = []
        self.encoded_data = []
        self.sections = []
        self.cities = []
        self.encode_dict = {}
        self.path_solve = node.PathSolve()

    def read_xls_file(self):
        xls_data = xlrd.open_workbook(self.f)
        table = xls_data.sheet_by_index(0)
        nrows = table.nrows
        for row_num in range(1, nrows):
            row = table.row_values(row_num)
            self.data.append(row)

    # staion names are encoded as numbers
    def encode(self):
        stations = []
        for rec in self.data:
            stations.append(rec[3])
        # get all stations with no repetition
        self.cities = set(stations)
        code = 1
        for city in self.cities:
            # encoding
            self.encode_dict[city] = str(code)
            code += 1
        for rec in self.data:
            # replace stations with corresponding codes
            rec[3] = self.encode_dict.get(rec[3])
            self.encoded_data.append(rec)

    def write(self):
        book = xlwt.Workbook()
        sheet1 = book.add_sheet('train')
        i = 0
        for data in self.encoded_data:
            row = sheet1.row(i)
            j = 0
            for a in data:
                row.write(j, a)
                j += 1
            i += 1
        book.save('120523_encoded.xls')

    # split routes into adjacent sections
    def split_trips(self):
        rec_idx = 0
        for rec in self.encoded_data:
            if rec[2] != 1.0:
                rec_pre = self.encoded_data[rec_idx - 1]
                section = rec_pre + rec
                section.append(rec[7] - rec_pre[7])
                self.sections.append(section)
            rec_idx += 1

    def sort(self):
        b = 0
        for section in self.sections:
            # b += 1
            # if b % 5 == 0:
            # 	print b
            f_station = section[3]
            t_station = section[11]
            dis = section[16]
            if self.is_recorded(f_station) and self.is_recorded(t_station):
                # if both recorded, find if any route link these nodes
                self.path_solve.solve(
                    f_station, None, f_station, t_station)
                # if no existing route links these nodes, record them
                if self.path_solve.paths is empty:
                    self.path_solve.nodes[f_station][t_station] = dis
                    self.path_solve.nodes[t_station][f_station] = dis
                # if nodes are linked by existing route(s)
                else:
                    is_dis_equal = False
                    for path in self.path_solve.paths:
                        if path[1] == dis:
                            is_dis_equal = True
                            break
                    # if the distances are not equal, record these nodes, if equal don not record
                    if not is_dis_equal:
                        self.path_solve.nodes[f_station][t_station] = dis
                        self.path_solve.nodes[t_station][f_station] = dis
                # if the two nodes seperate any existing sections
                self.path_solve.paths = []
                self.seperate(f_station, t_station, dis)
                self.seperate(t_station, f_station, dis)

            else:
                if not self.is_recorded(f_station):
                    self.path_solve.nodes[f_station] = {}
                    self.path_solve.nodes[f_station][t_station] = dis
                else:
                    self.path_solve.nodes[f_station][t_station] = dis
                if not self.is_recorded(t_station):
                    self.path_solve.nodes[t_station] = {}
                    self.path_solve.nodes[t_station][f_station] = dis
                else:
                    self.path_solve.nodes[t_station][f_station] = dis

    def seperate(self, code1, code2, dis1):
        # node1 = self.path_solve.nodes[code1]
        # seperate = False
        # for key1 in node1:
        # 	dis2 = node1[key1]
        # 	node2 = self.path_solve.nodes[key1]
        # 	for key2 in node2:
        # 		if key2 == code2:
        # 			if node2[key2] == dis1+dis2:
        # 				seperate = True
        # 				del self.path_solve.nodes[code2][key1]
        # 				del self.path_solve.nodes[key1][code2]
        # 				break
        # 	if seperate:
        # 		break
        seps = []
        for node1 in self.path_solve.nodes:
            for node2 in self.path_solve.nodes[node1]:
                if node1 == '183' and node2 == '102':
                    b = 1
                self.path_solve.solve(node1, None, node1, node2)
                dis = 0
                if len(self.path_solve.paths) > 1:
                    a = []
                    for p in self.path_solve.paths:
                        if len(p[0]) == 2:
                            dis = p[1]
                        else:
                            a.append(p[1])
                    for i in range(len(a)):
                        if a[i] == dis:
                            # if node2 == '138' or node1 == '138':
                            # 	b = 1
                            # print("000000000")
                            seps.append([node1, node2])
                self.path_solve.paths = []
        for s in seps:
            del self.path_solve.nodes[s[0]][s[1]]
        self.path_solve.paths = []

    def is_recorded(self, code):
        try:
            a = self.path_solve.nodes[code]
            return True
        except:
            return False


if __name__ == '__main__':
    fn = "data/120523.xls"
    train = TrainMtx(fn)
    train.read_xls_file()
    train.encode()
    train.write()
    # train.split_trips()
    # train.sort()
    # dis = 0
    # d = 0
    # for key1 in train.path_solve.nodes:
    #     for key2 in train.path_solve.nodes[key1]:
    #         dis += train.path_solve.nodes[key1][key2]
    # print(dis / 2)
    # # for sec in train.sections:
    # # 	d += sec[16]
    # # print d/2
    # nn = 0
    # for node in train.path_solve.nodes:
    #     # print node,
    #     # print ":",
    #     nn += len(train.path_solve.nodes[node])
    # print(nn / 2)

    # print(train.path_solve.nodes)
    # # a = 1
    # # nstations = len(train.cities)
    # # mtx2 = np.full((nstations, nstations), 0)
    # # for node in train.path_solve.nodes:
    # # 	for n in train.path_solve.nodes[node]:
    # # 		mtx2[int(node)-1][int(n)-1] = train.path_solve.nodes[node][n]
    # #
    # # np.savetxt('mtx2.csv', mtx2, delimiter=',')
