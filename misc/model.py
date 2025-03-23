from enum import StrEnum
from pydantic import BaseModel

class PackageType(StrEnum):
    """
    Represents different types of Composer packages.

    Package types are used for custom installation logic. If a package requires
    special handling, a custom type can be defined (e.g., `symfony-bundle`,
    `wordpress-plugin`, `typo3-cms-extension`). These types are specific to
    certain projects and require an appropriate installer.

    See Also:
        - Composer schema documentation: https://getcomposer.org/doc/04-schema.md#type

    Attributes:
        LIBRARY: The default type. Copies files to the vendor directory.
        PROJECT: Denotes a project rather than a library (e.g., Symfony app shells, CMS installers).
        METAPACKAGE: Contains only dependencies; no files are installed.
        COMPOSER_PLUGIN: Provides an installer for packages with a custom type.
        PLUGIN: Reserved for Composer plugins.
        PHP_EXT: Reserved for PHP extensions written in C.
        PHP_EXT_ZEND: Reserved for Zend PHP extensions written in C.
    """

    LIBRARY = "library"
    PROJECT = "project"
    METAPACKAGE = "metapackage"
    COMPOSER_PLUGIN = "composer-plugin"
    PLUGIN = "plugin"
    PHP_EXT = "php-ext"
    PHP_EXT_ZEND = "php-ext-zend"

class Downloads(BaseModel):
    daily: int
    total: int
    monthly: int
