<?php

use Symfony\Component\DependencyInjection\Argument\RewindableGenerator;

// This file has been auto-generated by the Symfony Dependency Injection Component for internal use.
// Returns the public 'form.type.product.shipping' shared service.

return $this->services['form.type.product.shipping'] = new \PrestaShopBundle\Form\Admin\Product\ProductShipping(${($_ = isset($this->services['translator']) ? $this->services['translator'] : $this->getTranslatorService()) && false ?: '_'}, ${($_ = isset($this->services['prestashop.adapter.legacy.context']) ? $this->services['prestashop.adapter.legacy.context'] : $this->getPrestashop_Adapter_Legacy_ContextService()) && false ?: '_'}, ${($_ = isset($this->services['prestashop.adapter.data_provider.warehouse']) ? $this->services['prestashop.adapter.data_provider.warehouse'] : ($this->services['prestashop.adapter.data_provider.warehouse'] = new \PrestaShop\PrestaShop\Adapter\Warehouse\WarehouseDataProvider())) && false ?: '_'}, ${($_ = isset($this->services['prestashop.adapter.data_provider.carrier']) ? $this->services['prestashop.adapter.data_provider.carrier'] : $this->load('getPrestashop_Adapter_DataProvider_CarrierService.php')) && false ?: '_'});
