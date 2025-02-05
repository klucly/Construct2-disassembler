from Parser import Parser
from util import extract_meta, get_data, save_decoded


# project_path = "../../Test project"
# project_path = "../../New project"
project_path = "../../source"
data_path = project_path + "/data.js"
c2runtime_path = project_path + "/c2runtime.js"


p = Parser(extract_meta(c2runtime_path))
a = p.parse(get_data(data_path))

output = "".join([str(i) for i in a])
save_decoded(output, "decoded.txt")
