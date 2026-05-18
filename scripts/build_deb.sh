#!/bin/bash
# Pulse Debian Package Builder
set -e

VERSION="0.2.0"
PKG_NAME="pulse-suite"
BUILD_DIR="build_deb"

echo "[*] Building Pulse .deb package v$VERSION..."

# Create structure
rm -rf $BUILD_DIR
mkdir -p $BUILD_DIR/DEBIAN
mkdir -p $BUILD_DIR/usr/bin
mkdir -p $BUILD_DIR/usr/share/pulse

# Create control file
cat <<EOC > $BUILD_DIR/DEBIAN/control
Package: $PKG_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Maintainer: Ekin Yuksel <ekinyuksel@example.com>
Description: Pulse: Unified Digital Identity Extractor for the AI Era.
 Depends: python3, python3-pip
EOC

# Copy source code
cp -r src/pulse $BUILD_DIR/usr/share/pulse/
cp pyproject.toml $BUILD_DIR/usr/share/pulse/

# Create entry point wrapper
cat <<EOW > $BUILD_DIR/usr/bin/pulse
#!/bin/bash
export PYTHONPATH="\$PYTHONPATH:/usr/share/pulse"
python3 -m pulse.cli "\$@"
EOW
chmod +x $BUILD_DIR/usr/bin/pulse

# Fix permissions
chmod -R 755 $BUILD_DIR

# Build the package
dpkg-deb --build $BUILD_DIR ${PKG_NAME}_${VERSION}_all.deb

echo "[+] Built: ${PKG_NAME}_${VERSION}_all.deb"
rm -rf $BUILD_DIR
