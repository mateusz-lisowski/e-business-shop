<?php

use Symfony\Component\DependencyInjection\Argument\RewindableGenerator;

// This file has been auto-generated by the Symfony Dependency Injection Component for internal use.
// Returns the public 'prestashop.admin.payment_preferences.form_data_provider' shared service.

return $this->services['prestashop.admin.payment_preferences.form_data_provider'] = new \PrestaShopBundle\Form\Admin\Improve\Payment\Preferences\PaymentPreferencesFormDataProvider(${($_ = isset($this->services['prestashop.adapter.payment_module_preferences.configuration']) ? $this->services['prestashop.adapter.payment_module_preferences.configuration'] : $this->load('getPrestashop_Adapter_PaymentModulePreferences_ConfigurationService.php')) && false ?: '_'});
