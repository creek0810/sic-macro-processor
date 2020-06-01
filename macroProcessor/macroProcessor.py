class MacroProcessor:
    def __init__(self, file_path):
        self.def_table = {}
        self.path = file_path

    def _is_comment(self, cur_line):
        return cur_line.startswith(".")

    def _is_macro_def(self, cur_line):
        split_data = cur_line.split()
        return len(split_data) >= 2 and split_data[1] == "MACRO"


    # return name of current macro call
    def _parse_name(self, cur_line):
        split_data = cur_line.split()
        return (
            split_data[0] if split_data[0] in self.def_table else split_data[1]
        )

    #  TODO: finish here
    def _is_macro_call(self, cur_line):
        split_data = cur_line.split()

        # general macro call
        if len(split_data) >= 2:
            return (
                split_data[0] in self.def_table
                or split_data[1] in self.def_table
            )
        # no label no arg macro call
        elif len(split_data) >= 1:
            return split_data[0] in self.def_table
        return False

    def _parse_arg(self, cur_line):
        if self._is_macro_def(cur_line):

            return cur_line.replace(",", " ").split()[2:]

        macro_name = self._parse_name(cur_line)
        split_data = cur_line.strip().replace(",", " ").split()
        start = split_data.index(macro_name) + 1
        return split_data[start:]


    def _expand_macro(self, lines, i):
        cur_line = lines[i]

        # print comment
        comment = cur_line.lstrip()
        print(f".{comment}")

        # if cur_line has label
        label = cur_line.split()[0]
        if label not in self.def_table:
            print(label, end=" ")

        # start expand
        cur_arg = self._parse_arg(cur_line)
        macro_name = self._parse_name(cur_line)

        cur_macro = self.def_table[macro_name]

        i = 0
        while i < len(cur_macro["body"]):
            cur_line = cur_macro["body"][i]
            # define the macro which is defined in macro
            if self._is_macro_def(cur_line):
                i = self._define_macro(cur_macro["body"], i)
            # general instruction
            else:
                # replace arg
                for idx, arg in enumerate(cur_macro["arg"]):
                    cur_line = cur_line.replace(arg, cur_arg[idx])
                print(cur_line)
                i += 1


    def _define_macro(self, lines, i):
        macro_body = []
        macro_name = lines[i].split()[0]
        macro_arg = self._parse_arg(lines[i])

        level = 1

        # i = a var to iterate lines
        # skip first line
        i += 1
        # construct macro body
        while level > 0:
            cur_line = lines[i]
            i += 1

            # skip comment
            if self._is_comment(cur_line):
                continue

            split_data = cur_line.split()
            macro_body.append(cur_line)
            if self._is_macro_def(cur_line):
                level += 1
            elif len(split_data) >= 1 and split_data[0] == "MEND":
                level -= 1
        # update def table
        self.def_table[macro_name] = {
            "arg": macro_arg,
            # delete last MEND instruction
            "body": macro_body[:-1]
        }
        # return cur line num
        return i

    def process(self):
        with open(self.path, "r") as file:
            raw_data = file.readlines()
            lines = [x.replace("\n", "") for x in raw_data]
            i = 0
            while i < len(lines):
                cur_line = lines[i]
                # skip comment
                if self._is_comment(cur_line):
                    i += 1
                # define macro
                elif self._is_macro_def(cur_line):
                    i = self._define_macro(lines, i)
                # expand macro
                elif self._is_macro_call(cur_line):
                    self._expand_macro(lines, i)
                    i += 1
                # general instruction
                else:
                    print(lines[i])
                    i += 1
