<?php

// This file has been auto-generated by the Symfony Dependency Injection Component for internal use.

if (\class_exists(\ContainerNk0baax\appDevDebugProjectContainer::class, false)) {
    // no-op
} elseif (!include __DIR__.'/ContainerNk0baax/appDevDebugProjectContainer.php') {
    touch(__DIR__.'/ContainerNk0baax.legacy');

    return;
}

if (!\class_exists(appDevDebugProjectContainer::class, false)) {
    \class_alias(\ContainerNk0baax\appDevDebugProjectContainer::class, appDevDebugProjectContainer::class, false);
}

return new \ContainerNk0baax\appDevDebugProjectContainer([
    'container.build_hash' => 'Nk0baax',
    'container.build_id' => 'ca3307ae',
    'container.build_time' => 1736790448,
], __DIR__.\DIRECTORY_SEPARATOR.'ContainerNk0baax');
