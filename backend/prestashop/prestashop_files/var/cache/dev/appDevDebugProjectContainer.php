<?php

// This file has been auto-generated by the Symfony Dependency Injection Component for internal use.

if (\class_exists(\ContainerMxm98qg\appDevDebugProjectContainer::class, false)) {
    // no-op
} elseif (!include __DIR__.'/ContainerMxm98qg/appDevDebugProjectContainer.php') {
    touch(__DIR__.'/ContainerMxm98qg.legacy');

    return;
}

if (!\class_exists(appDevDebugProjectContainer::class, false)) {
    \class_alias(\ContainerMxm98qg\appDevDebugProjectContainer::class, appDevDebugProjectContainer::class, false);
}

return new \ContainerMxm98qg\appDevDebugProjectContainer([
    'container.build_hash' => 'Mxm98qg',
    'container.build_id' => '3fb1cd59',
    'container.build_time' => 1733082317,
], __DIR__.\DIRECTORY_SEPARATOR.'ContainerMxm98qg');
