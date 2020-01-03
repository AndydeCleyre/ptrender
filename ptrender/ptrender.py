import sys

from collections import defaultdict
from json import loads as jloads

from plumbum import local, LocalPath
from plumbum.cli import (
    Application,
    ExistingDirectory,
    ExistingFile,
    Flag,
    NonexistentPath,
    SwitchAttr
)
from plumbum.colors import red, yellow
from pyratemp import Template

from . import __version__


def warn(msg):
    print(msg | yellow, file=sys.stderr)


def err(msg):
    print(msg | red, file=sys.stderr)


try:
    import strictyaml
except ModuleNotFoundError:
    warn("Install strictyaml (or 'ptrender[yaml]') with pip for yaml support")


def yloads(yml):
    return strictyaml.load(yml).data


def warn_overrides(var_mentions: dict):
    for var, files in var_mentions.items():
        if len(files) > 1:
            warn(f"Be warned! {var} is overridden: {files}")


def warn_shebangs(template_file: LocalPath):
    for line in template_file.read().splitlines():
        if '#!/' in line:
            warn(
                f"Be warned! Template includes '{line}', "
                "which includes what pyratemp considers a template comment, "
                "to be omitted from the rendered output. "
                "\nTo fix, replace '#!' with '#@!!@!'."
            )


class TemplateRenderer(Application):
    """
    Use json or yaml var_files to render template_file to an adjacent
    file with the same name but the extension stripped
    """

    VERSION = __version__

    overwrite = Flag(
        ['f', 'force'],
        help="Overwrite any existing destination file"
    )

    def main(self, template_file: ExistingFile, *var_files: ExistingFile):
        warn_shebangs(template_file)
        data = {}  # {var: value}
        var_mentions = defaultdict(list)  # {var: [files]}
        for vfile in var_files:
            loader = jloads if vfile.suffix.lower() == '.json' else yloads
            new_data = loader(vfile.read())
            for v in new_data:
                var_mentions[v].append(vfile)
            data.update(new_data)
        warn_overrides(var_mentions)
        rstr = Template(filename=str(template_file), data=data)()
        dest = template_file.with_suffix('')
        if not self.overwrite:
            try:
                NonexistentPath(dest)
            except ValueError as e:
                err(f"{type(e)}: {e}")
                err("Use -f/--force to overwrite")
                sys.exit(1)
        dest.write(rstr)


class VWriter(Application):
    """
    Use json or yaml vars files to render each template file found recursively
    under the working folder, to an adjacent file with the same name but the
    extension stripped, overriding any vars in ./vars.json in the following
    order:

        <root_path>/vars.json,
        <root_path>/vars.yml,
        <root_path>/vars.yaml,
        <template.parent>/vars.json,
        <template.parent>/vars.yml,
        <template.parent>/vars.yaml

    Later entries override earlier ones.
    """

    VERSION = __version__

    overwrite = Flag(
        ['f', 'force'],
        help="Overwrite any existing destination file"
    )
    template_ext = SwitchAttr(
        ['t', 'template-ext'],
        help="Filename extension for templates",
        default='t'
    )
    vars_name = SwitchAttr(
        ['n', 'vars-name'],
        help="Filename (excluding extension) for each vars file",
        default='vars'
    )

    ext_precedence = ('json', 'yml', 'yaml')

    def get_vars_files(self, folder: ExistingDirectory):
        return [
            folder / f"{self.vars_name}.{ext}"
            for ext in self.ext_precedence
            if (folder / f"{self.vars_name}.{ext}").is_file()
        ]

    def main(self, root_path: ExistingDirectory=local.cwd):
        """root_path defaults to the process's working directory"""
        root_vfiles = self.get_vars_files(root_path)
        for tmplt in root_path.walk(lambda f: f.suffix == f".{self.template_ext}"):
            if tmplt.up() == root_path:
                vfiles = root_vfiles
            else:
                vfiles = (*root_vfiles, *self.get_vars_files(tmplt.up()))
            TemplateRenderer.invoke(tmplt, *vfiles, overwrite=self.overwrite)
