<?php

// This file has been auto-generated by the Symfony Dependency Injection Component for internal use.

if (\class_exists(\ContainerMd77xz2\appDevDebugProjectContainer::class, false)) {
    // no-op
} elseif (!include __DIR__.'/ContainerMd77xz2/appDevDebugProjectContainer.php') {
    touch(__DIR__.'/ContainerMd77xz2.legacy');

    return;
}

if (!\class_exists(appDevDebugProjectContainer::class, false)) {
    \class_alias(\ContainerMd77xz2\appDevDebugProjectContainer::class, appDevDebugProjectContainer::class, false);
}

return new \ContainerMd77xz2\appDevDebugProjectContainer([
    'container.build_hash' => 'Md77xz2',
    'container.build_id' => '2c144f2e',
    'container.build_time' => 1732307046,
], __DIR__.\DIRECTORY_SEPARATOR.'ContainerMd77xz2');