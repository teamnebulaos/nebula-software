project('nebula-software',
        version: '1.0.0',
        meson_version: '>= 0.59.0',
        default_options: ['warning_level=2'])

dependency('gtk4')
dependency('libadwaita-1')
dependency('json-glib-1.0')
dependency('libsoup-3.0')

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'nebula_software')

subdir('data')
subdir('src')
