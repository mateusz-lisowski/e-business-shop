<?php

use Symfony\Component\DependencyInjection\Argument\RewindableGenerator;

// This file has been auto-generated by the Symfony Dependency Injection Component for internal use.
// Returns the public 'PrestaShop\Module\PsxMarketingWithGoogle\ProductFilter\Options\BrandOptionsProvider' shared service.

return $this->services['PrestaShop\\Module\\PsxMarketingWithGoogle\\ProductFilter\\Options\\BrandOptionsProvider'] = new \PrestaShop\Module\PsxMarketingWithGoogle\ProductFilter\Options\BrandOptionsProvider(${($_ = isset($this->services['PrestaShop\\Module\\PsxMarketingWithGoogle\\Repository\\ManufacturerRepository']) ? $this->services['PrestaShop\\Module\\PsxMarketingWithGoogle\\Repository\\ManufacturerRepository'] : $this->load('getManufacturerRepository2Service.php')) && false ?: '_'});
