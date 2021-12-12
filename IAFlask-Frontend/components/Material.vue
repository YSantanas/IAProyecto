<template>
  <div>
    <b-container class="mt-3">
      <b-row align-h="center">
        <b-col cols="12" md="8" lg="9" class="text-center">
          <b-img src="@/assets/logo.png" fluid></b-img>
        </b-col>
      </b-row>

      <b-row align-h="center">
        <b-col cols="8">
          <h1 class="text-center text-info">
            Material
          </h1>

          <p class="p-3 bg-secondary text-white">
            En el siguiente pdf podermos ver la unificación de toda la teoría utilizada dentro del curso para elaborar este proyecto.
          </p>
      <iframe
        src="http://localhost:5000/static/documentos/generados/TeoriaDelCurso.pdf"
        width="680"
        height="780"
        style="border: none"
      ></iframe>

        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
export default {}
</script>
