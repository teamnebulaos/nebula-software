python = import('python')

py_installation = python.find_installation('python3')

conf = configuration_data()
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)
conf.set('moduledir', moduledir)

configure_file(
  input: 'nebula-software.in',
  output: 'nebula-software',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

nebula_software_sources = [
  'main.py',
  'window.py',
]

install_data(nebula_software_sources, install_dir: moduledir)
