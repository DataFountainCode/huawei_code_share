import csv
import os

res = {}

def get_annotations(path):
  with open(path, "r") as f:
    reader = csv.reader(f)
    for item in reader:
      if not item[0].endswith('jpg'):
        continue
      if item[0] not in res:
        res[item[0]] = []
      res[item[0]].append(item[1:])
  return res

def write_txt(d, path):
  for name, objects in d.items():
    name = name.split('.')[0] + '.txt'
    with open(os.path.join(path, name), 'w') as f:
      for ob in objects:
        f.write(','.join(ob) + '\n')


if __name__ == '__main__':
  path = 'D:/data/chinese/train_lable.csv'
  save_path = 'D:/data/chinese/trian_dataset/'
  d = get_annotations(path)
  write_txt(d, save_path)
