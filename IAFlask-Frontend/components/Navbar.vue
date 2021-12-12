<template>
  <div>
    <b-navbar type="dark" variant="primary">
      <b-navbar-nav>
        <img
          src="https://drive.google.com/uc?export?view&id=1fEp-54Ndizp49J_yrMyetXr5buBbMOf5"
          width="30"
          height="30"
          class="d-inline-block align-top"
          alt=""
        />

        <b-nav-item href="/">Inicio</b-nav-item>
        <b-nav-item href="/material">Material</b-nav-item>
        <!-- Navbar dropdowns -->

        <b-nav-item-dropdown text="Ejercicios" right>
          <b-dropdown-item href="/apriori">Apriori</b-dropdown-item>
          <b-dropdown-item href="/metrica">Metricas Distancia</b-dropdown-item>
          <b-dropdown-item href="/cluster">Cluster Jerarquico</b-dropdown-item>
          <b-dropdown-item href="/clusterP"
            >Cluster Particional</b-dropdown-item
          >
          <b-dropdown-item href="/regresionLineal"
            >Regresión Lineal Multiple</b-dropdown-item
          >
          <b-dropdown-item href="/ClasificacionRL"
            >Clasificación con RL</b-dropdown-item
          >
          <b-dropdown-item href="/pronosticoArbol"
            >Pronostico Arbol</b-dropdown-item
          >
          <b-dropdown-item href="/clasificacionArbol"
            >Clasificación Arbol</b-dropdown-item
          >
        </b-nav-item-dropdown>

        <b-nav-item href="/contacto">Contacto</b-nav-item>
      </b-navbar-nav>
    </b-navbar>
  </div>
</template>

<style>
/* cambiar tipo de letra */
a.nav-link.nuxt-link-exact-active.nuxt-link-active {
  color: white !important;
}
</style>
