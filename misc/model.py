from enum import StrEnum
from typing import Optional, Union, List, Dict

from pydantic import BaseModel, constr


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


class Maintainer(BaseModel):
    """
    Represents a maintainer of a package.

    Attributes:
        name (str): The name of the maintainer.
        avatar_url (str): The URL of the maintainer's avatar image.
    """
    name: str
    avatar_url: str


class Downloads(BaseModel):
    """
    Represents the download statistics of a package.

    Attributes:
        daily (int): The number of daily downloads.
        total (int): The total number of downloads.
        monthly (int): The number of monthly downloads.
    """
    daily: int
    total: int
    monthly: int


class Author(BaseModel):
    """
    Represents an author of a package.

    See Also:
        - https://github.com/composer/packagist/blob/dee836ff759c333a57c4eb93178c34d091adc87e/src/Entity/Version.php#L34

    Attributes:
        email (Optional[str]): The email address of the author.
        homepage (Optional[str]): The homepage URL of the author.
        name (Optional[str]): The name of the author.
        role (Optional[str]): The role of the author.
    """
    email: Optional[str] = None
    homepage: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None


class PhpExtOptions(BaseModel):
    """
    Represents configuration options for a PHP extension.

    See Also:
        - https://github.com/composer/packagist/blob/dee836ff759c333a57c4eb93178c34d091adc87e/src/Entity/Version.php#L54

    Attributes:
        name (str): The name of the configuration option.
        description (Optional[str]): A description of the configuration option.
    """
    name: str
    description: Optional[str] = None


class PhpExt(BaseModel):
    """
    Represents a PHP extension.

    See Also:
        - https://github.com/composer/packagist/blob/dee836ff759c333a57c4eb93178c34d091adc87e/src/Entity/Version.php#L54

    Attributes:
        priority (Optional[int]): The priority of the PHP extension.
        configure_options (Optional[List[PhpExtOptions]]): The configuration options for the PHP extension.
    """
    priority: Optional[int] = None
    configure_options: Optional[List[PhpExtOptions]] = None


class Version(BaseModel):
    """
    Represents a version of a package.

    See Also:
        - https://github.com/composer/packagist/blob/dee836ff759c333a57c4eb93178c34d091adc87e/src/Entity/Version.php

    Attributes:
        name (str): The name of the version.
        description (str): A description of the version.
        keywords (List[str]): A list of keywords associated with the version.
        homepage (str): The homepage URL of the version.
        version (constr): The version string.
        version_normalized (constr): The normalized version string.
        license (List[str]): A list of licenses for the version.
        authors (List[Author]): A list of authors of the version.
        source (Dict): The source information of the version.
        dist (Dict): The distribution information of the version.
        type (Optional[Union[str, None]]): The type of the version.
        support (Optional[Dict]): The support information of the version.
        funding (Optional[Dict]): The funding information of the version.
        time (Optional[str]): The release time of the version.
        autoload (Optional[Dict]): The autoload configuration of the version.
        extra (Optional[Dict]): Additional information about the version.
        target_dir (Optional[str]): The target directory for the version.
        include_path (Optional[List[str]]): The include paths for the version.
        bin (Optional[List[str]]): The binary files for the version.
        default_branch (Optional[bool]): Whether this version is the default branch.
        require (Optional[Dict[str, str]]): The required dependencies for the version.
        require_dev (Optional[Dict[str, str]]): The development dependencies for the version.
        suggest (Optional[Dict[str, str]]): The suggested packages for the version.
        conflict (Optional[Dict[str, str]]): The conflicting packages for the version.
        provide (Optional[Dict[str, str]]): The provided packages for the version.
        replace (Optional[Dict[str, str]]): The replaced packages for the version.
        abandoned (Optional[Union[str, bool]]): Whether the version is abandoned.
        php_ext (Optional[PhpExt]): The PHP extension information for the version.
    """
    name: str
    description: str
    keywords: List[str]
    homepage: str
    version: constr(min_length=1)
    version_normalized: constr(min_length=1)
    license: List[str]
    authors: List[Author]
    source: Dict
    dist: Dict
    type: Optional[Union[str, None]] = None
    support: Optional[Dict] = None
    funding: Optional[Dict] = None
    time: Optional[str] = None
    autoload: Optional[Dict] = None
    extra: Optional[Dict] = None
    target_dir: Optional[str] = None
    include_path: Optional[List[str]] = None
    bin: Optional[List[str]] = None
    default_branch: Optional[bool] = None
    require: Optional[Dict[str, str]] = None
    require_dev: Optional[Dict[str, str]] = None
    suggest: Optional[Dict[str, str]] = None
    conflict: Optional[Dict[str, str]] = None
    provide: Optional[Dict[str, str]] = None
    replace: Optional[Dict[str, str]] = None
    abandoned: Optional[Union[str, bool]] = None
    php_ext: Optional[PhpExt] = None


class Package(BaseModel):
    """
    Represents a package.

    See Also:
        - https://github.com/composer/packagist/blob/dee836ff759c333a57c4eb93178c34d091adc87e/src/Entity/Package.php

    Attributes:
        name (str): The name of the package.
        description (Optional[str]): A description of the package.
        time (str): The time the package was created.
        maintainers (List[Maintainer]): A list of maintainers of the package.
        versions (List[Version]): A list of versions of the package.
        type (Optional[PackageType]): The type of the package.
        repository (str): The repository URL of the package.
        github_stars (Optional[int]): The number of GitHub stars.
        github_watchers (Optional[int]): The number of GitHub watchers.
        github_forks (Optional[int]): The number of GitHub forks.
        github_open_issues (Optional[int]): The number of open issues on GitHub.
        language (Optional[str]): The programming language of the package.
        abandoned (Optional[Union[str, bool]]): Whether the package is abandoned.
        dependents (Optional[int]): The number of dependents.
        suggesters (Optional[int]): The number of suggesters.
        downloads (Downloads): The download statistics of the package.
        favers (Optional[int]): The number of users who have favored the package.
    """
    name: str
    description: Optional[str] = None
    time: str
    maintainers: List[Maintainer]
    versions: List[Version]
    type: Optional[PackageType] = None
    repository: str
    github_stars: Optional[int] = None
    github_watchers: Optional[int] = None
    github_forks: Optional[int] = None
    github_open_issues: Optional[int] = None
    language: Optional[str] = None
    abandoned: Optional[Union[str, bool]] = None
    dependents: Optional[int] = None
    suggesters: Optional[int] = None
    downloads: Downloads
    favers: Optional[int] = None
