from datetime import datetime
from enum import StrEnum
from typing import Optional, Union, List, Dict

from pydantic import BaseModel, constr, HttpUrl


class PackageType(StrEnum):
    METAPACKAGE = "metapackage"
    COMPOSER_PLUGIN = "composer-plugin"
    PLUGIN = "plugin"
    PHP_EXT = "php-ext"
    PHP_EXT_ZEND = "php-ext-zend"
    PROJECT = "project"
    LIBRARY = "library"


class Maintainer(BaseModel):
    name: str
    avatar_url: HttpUrl


class Downloads(BaseModel):
    daily: int
    total: int
    monthly: int


class Author(BaseModel):
    email: Optional[str] = None
    homepage: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None


class PhpExtOptions(BaseModel):
    name: str
    description: Optional[str] = None


class PhpExt(BaseModel):
    priority: Optional[int] = None
    configure_options: Optional[List[PhpExtOptions]] = None


class Version(BaseModel):
    name: str
    description: str
    version: constr(min_length=1)
    version_normalized: constr(min_length=1)
    license: List[str]
    authors: List[Author]
    type: Optional[PackageType] = None
    time: Optional[datetime] = None
    default_branch: Optional[bool] = None
    require: Optional[Dict[str, str]] = None
    require_dev: Optional[Dict[str, str]] = None
    suggest: Optional[Dict[str, str]] = None
    conflict: Optional[Dict[str, str]] = None
    provide: Optional[Dict[str, str]] = None
    replace: Optional[Dict[str, str]] = None
    abandoned: Optional[Union[str, bool]] = None

    def aggregate_require(self) -> list:
        return list({r for r in self.require.keys()}) if self.require else []

    def aggregate_require_dev(self) -> list:
        return list({r for r in self.require_dev.keys()}) if self.require_dev else []

    def aggregate_suggest(self) -> list:
        return list({s for s in self.suggest.keys()}) if self.suggest else []

    def aggregate_conflict(self) -> list:
        return list({c for c in self.conflict.keys()}) if self.conflict else []

    def aggregate_provide(self) -> list:
        return list({p for p in self.provide.keys()}) if self.provide else []

    def aggregate_replace(self) -> list:
        return list({r for r in self.replace.keys()}) if self.replace else []


class Package(BaseModel):
    name: str
    description: Optional[str] = None
    time: datetime
    maintainers: List[Maintainer]
    type: Optional[PackageType] = None
    repository: Optional[HttpUrl] = None
    github_stars: Optional[int] = None
    github_watchers: Optional[int] = None
    github_forks: Optional[int] = None
    github_open_issues: Optional[int] = None
    language: Optional[str] = None
    abandoned: Optional[Union[str, bool]] = None
    dependents: Optional[int] = None
    suggesters: Optional[int] = None
    downloads: Downloads
    versions: Dict[str, Version]

    def aggregate_versions(self) -> list:
        return list({v.version_normalized for v in self.versions.values()})

    def aggregate_licenses(self) -> list:
        return list({l for version in self.versions.values() for l in version.license})

    def aggregate_authors(self) -> list:
        return list({a.name for version in self.versions.values() for a in version.authors})

    def last_updated_time(self) -> datetime:
        return max([v.time for v in self.versions.values()])

    def aggregate_require(self) -> list:
        return list({r for version in self.versions.values() for r in version.aggregate_require()})

    def aggregate_require_dev(self) -> list:
        return list({r for version in self.versions.values() for r in version.aggregate_require_dev()})

    def aggregate_suggest(self) -> list:
        return list({s for version in self.versions.values() for s in version.aggregate_suggest()})

    def aggregate_conflict(self) -> list:
        return list({c for version in self.versions.values() for c in version.aggregate_conflict()})

    def aggregate_provide(self) -> list:
        return list({p for version in self.versions.values() for p in version.aggregate_provide()})

    def aggregate_replace(self) -> list:
        return list({r for version in self.versions.values() for r in version.aggregate_replace()})
