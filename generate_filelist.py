import argparse
import os
import glob
def createLabVIVOS(args):
    in_dir = os.path.join(args.base_dir)
    out_dir = in_dir
    dict_valid = {

    }

    dict_train = {

    }
    print(in_dir)
    dirs = ["test", "train"]
    for dir in dirs:
        with open(os.path.join(in_dir, dir, 'genders.txt'), encoding='utf-8') as g:
            for line in g:
                if line[0] != 'S':
                    line = line[0:]
                parts = line.strip().split(' ')
                if dir == "test":
                    dict_valid[parts[0]] = parts[1]
                else:
                    dict_train[parts[0]] = parts[1]

    for dir in dirs:
        with open(os.path.join(in_dir, dir, 'prompts.txt'), encoding='utf-8') as f:
            for line in f:
                if line[0] != 'S':
                    line = line[0:]
                delIdx = line.index(" ")
                gender = ""
                if dir == "test":
                    gender = dict_valid[line[0:10]]
                else:
                    gender = dict_train[line[0:10]]
                name = line[0:delIdx]
                prompt = line[delIdx + 1: len(line) - 1]
                if gender == "f":
                    # out_dir = os.path.join(in_dir, 'lab_f')
                    if dir == "test":
                        with (open(os.path.join(".\\filelists", "vivos_female_val.txt"), 'a+', encoding='utf-8')) as pm:
                            pm.write("vivos/test/waves/" + name[0:10] + "/" + name + ".wav" + "|" + prompt + "\n")
                    else:
                        with (open(os.path.join(".\\filelists", "vivos_female_train.txt"), 'a+', encoding='utf-8')) as pm:
                            pm.write("vivos/train/waves/" + name[0:10] + "/" + name + ".wav" + "|" + prompt + "\n")
                else:
                    if dir == "test":
                        with (open(os.path.join(".\\filelists", "vivos_male_val.txt"), 'a+', encoding='utf-8')) as pm:
                            pm.write("vivos/test/waves/" + name[0:10] + "/" + name + ".wav" + "|" + prompt + "\n")
                    else:
                        with (open(os.path.join(".\\filelists", "vivos_male_train.txt"), 'a+', encoding='utf-8')) as pm:
                            pm.write("vivos/train/waves/" + name[0:10] + "/" + name + ".wav" + "|" + prompt + "\n")
                    # out_dir = os.path.join(in_dir, 'lab_m')

            # parts = line.strip().split(',')

            # text = parts[1].replace('\t',', ')
            # with open(os.path.join(out_dir, '%s.txt' %name), 'w', encoding="utf-8") as t:
            #     t.write(prompt)

            # with (open(os.path.join(in_dir, "prompt_no_title.txt"), 'a', encoding = 'utf-8')) as pnt:
            #     pnt.write(prompt + "\n  ")

def createLabVIVOS2(args):
    in_train_dir = os.path.join(args.train_dir)
    in_test_dir = os.path.join(args.test_dir)
    os.makedirs(os.path.dirname(args.train_filelist_out), exist_ok=True)
    os.makedirs(os.path.dirname(args.test_filelist_out), exist_ok=True)

    #generate train filelist
    for wavfile in glob.glob(os.path.join(in_train_dir, '*.wav')):
        with open(os.path.join(os.getcwd(), wavfile), 'r') as f:
            wavfile = wavfile.replace("\\", "/")
            record = wavfile + "|"
            with open(os.path.join(os.path.splitext(wavfile)[0] + ".txt"), encoding='utf-8', mode='r') as prompt:
                record += prompt.readlines()[0]

            with open(os.path.join(args.train_filelist_out), encoding="utf-8", mode="a") as out:
                out.write(record + "\n")

    #generate test filelist
    for wavfile in glob.glob(os.path.join(in_test_dir, '*.wav')):
        with open(os.path.join(os.getcwd(), wavfile), 'r') as f:
            wavfile = wavfile.replace("\\", "/")
            record = wavfile + "|"
            with open(os.path.join(os.path.splitext(wavfile)[0] + ".txt"), encoding='utf-8', mode='r') as prompt:
                record += prompt.readlines()[0]

            with open(os.path.join(args.test_filelist_out), encoding="utf-8", mode="a") as out:
                out.write(record + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_dir', default=os.path.expanduser('vivos/22050/train/wavs_m_22050'))
    parser.add_argument('--test_dir', default=os.path.expanduser('vivos/22050/test/wavs_m_22050'))
    parser.add_argument('--prompt',default=os.path.expanduser('vivos/22050/prompt.txt'))
    parser.add_argument('--train_filelist_out', default="filelists/vivos/22050/male/train2.txt")
    parser.add_argument('--test_filelist_out',default="filelists/vivos/22050/male/test2.txt")
    args = parser.parse_args()

    # createLab(args)
    createLabVIVOS2(args);


if __name__ == "__main__":
    main()