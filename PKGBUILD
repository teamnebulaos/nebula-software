# Maintainer: NebulaOS Team
pkgname=nebula-software
pkgver=1.0.0
pkgrel=1
pkgdesc="Software Update Manager for NebulaOS"
arch=('x86_64')
url="https://github.com/teamnebulaos/nebula-software"
license=('GPL3')
depends=('gtk4' 'libadwaita' 'python-gobject' 'python-requests')
makedepends=('meson' 'ninja' 'git')
source=("git+https://github.com/teamnebulaos/nebula-software.git")
sha256sums=('SKIP')

build() {
    cd "$pkgname"
    arch-meson build
    meson compile -C build
}

package() {
    cd "$pkgname"
    DESTDIR="$pkgdir" meson install -C build
}
