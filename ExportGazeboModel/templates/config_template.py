from string import Template

class ConfigTemplate:
    template = Template(
        """\
<?xml version="1.0" ?>
<model>
    <name>${model_name}</name>
    <version>1.0</version>
    <sdf version="1.6">model.sdf</sdf>
    <author>
        <name>${author_name}</name>
        <email>${author_email}</email>
    </author>
    <description></description>
</model>\
    """
    )