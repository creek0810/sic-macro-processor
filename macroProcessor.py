class MacroProcessor:
    def __init__(self, file_path):
        self.def_table = {}
        self.path = file_path

    def _is_comment(self, cur_line):
        return cur_line.startswith(".")

    def _is_macro_def(self, split_data):
        return len(split_data) >= 2 and split_data[1] == "MACRO"

    def _is_macro_call(self, split_data):
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
        if self._is_macro_def(cur_line.split()):

            return cur_line.replace(",", "").split()[2:]

        macro_name = self._parse_name(cur_line)
        split_data = cur_line.strip().replace(",", " ").split()
        start = split_data.index(macro_name) + 1
        return split_data[start:]

    # return name of current macro call
    def _parse_name(self, cur_line):
        split_data = cur_line.split()
        return (
            split_data[0] if split_data[0] in self.def_table else split_data[1]
        )

    def _expand(self, cur_line):
        # print comment line
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
        for cur_body_line in cur_macro["body"]:
            result = cur_body_line

            # replace arg
            for idx, arg in enumerate(cur_macro["arg"]):
                result = result.replace(arg, cur_arg[idx])
            print(result)

    # establish def_table
    def _pass1(self):
        with open(self.path, "r") as file:
            # macro info
            is_macro = False
            macro_name = ""
            macro_body = []
            macro_arg = []

            for cur_line in file.readlines():
                cur_line = cur_line.replace("\n", "")

                if self._is_comment(cur_line):
                    continue

                split_data = cur_line.split()
                # start record macro
                if self._is_macro_def(split_data):
                    is_macro = True
                    macro_name = split_data[0]
                    macro_arg = self._parse_arg(cur_line)
                # update def_table
                elif len(split_data) >= 1 and split_data[0] == "MEND":
                    self.def_table[macro_name] = {
                        "body": macro_body,
                        "arg": macro_arg,
                    }
                    # clear macro_body and macro_arg
                    macro_body = []
                    macro_arg = []
                    is_macro = False

                elif is_macro:
                    macro_body.append(cur_line)

    def _pass2(self):
        with open(self.path, "r") as file:
            # this flag used to ignore macro
            is_macro = False
            for cur_line in file.readlines():
                cur_line = cur_line.replace("\n", "")
                if self._is_comment(cur_line):
                    continue

                split_data = cur_line.split()
                if self._is_macro_def(split_data):
                    is_macro = True
                elif len(split_data) >= 1 and split_data[0] == "MEND":
                    is_macro = False
                elif is_macro:
                    continue
                elif self._is_macro_call(split_data):
                    self._expand(cur_line)
                else:
                    print(cur_line)

    def process(self):
        self._pass1()
        self._pass2()
