# Copyright (c) 2020 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
This hook is used override some of the functionality of the :class:`~sgtk.bootstrap.ToolkitManager`.

It will be instantiated only after a configuration has been selected by the :class:`~sgtk.bootstrap.ToolkitManager`.
Therefore, this hook will not be invoked to download a configuration. However, the Toolkit Core,
applications, frameworks and engines can be downloaded through the hook.
"""

from sgtk import get_hook_baseclass


class RegisterDescriptors(get_hook_baseclass()):
    def init(
        self, shotgun, pipeline_configuration_id, configuration_descriptor, **kwargs
    ):
        """
        Initializes the hook.

        This method is called right after the bootstrap manager reads this hook and passes in
        information about the pipeline configuration that will be used.

        The default implementation copies the arguments into the attributes named ``shotgun``,
        ``pipeline_configuration_id`` and ``configuration_descriptor``.

        Additional attributes of note are ``io_descriptor_base``
            which are the base classes that you register types against using the
            ``register_descriptor_factory`` method.

        :param shotgun: Connection to the Shotgun site.
        :type shotgun: :class:`~shotgun_api3.Shotgun`

        :param int pipeline_configuration_id: Id of the pipeline configuration we're bootstrapping into.
            If None, the ToolkitManager is bootstrapping into the base configuration.

        :param configuration_descriptor: Configuration the manager is bootstrapping into.
        :type configuration_descriptor: :class:`~sgtk.descriptor.ConfigDescriptor`
        """
        self.shotgun = shotgun
        self.pipeline_configuration_id = pipeline_configuration_id
        self.configuration_descriptor = configuration_descriptor

        from sgtk.descriptor.io_descriptor.base import IODescriptorBase

        self.io_descriptor_base = IODescriptorBase

    def register_io_descriptors(self):
        """
        Register the IODescriptor subclasses with the IODescriptorBase factory.
        This complex process for handling the IODescriptor abstract factory
        management is in order to avoid local imports in classes.
        """
        from sgtk.descriptor.io_descriptor import _initialize_descriptor_factory

        _initialize_descriptor_factory(self.io_descriptor_base)
