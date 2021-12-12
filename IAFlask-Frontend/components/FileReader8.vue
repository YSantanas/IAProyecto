<template>
  <b-container>
    <b-row align-h="center">
      <b-col cols="12" md="8" lg="9" class="text-center">
        <b-img src="@/assets/logo.png" fluid></b-img>
      </b-col>
    </b-row>
    <h1 class="row justify-content-center">
      Clasificación con <small> Regresión Logística</small>
    </h1>

    <b-row class="my-4" align-h="center">
      <b-col cols="3">
        <b-row>
          <b-form-file ref="file" v-model="file" />
          <b-form-input
            v-model="variableEvalCRL"
            type="text"
            placeholder="variable de Eval"
          />

          <b-form-input
            v-model="porcentajeCRL"
            type="number"
            :step="0.01"
            placeholder="Porcentaje"
          />
          <p class="p-3 mb-2 bg-dark text-white text-center">
            Datos para nuevos pronosticos
          </p>
          <b-form-input v-model="Texture" type="number" placeholder="Textura" />
          <b-form-input
            v-model="Perimeter"
            type="number"
            placeholder="Perimetro"
          />
          <b-form-input
            v-model="Smoothness"
            type="number"
            placeholder="Suavidad"
          />
          <b-form-input
            v-model="Compactness"
            type="number"
            placeholder="Compacidad"
          />
          <b-form-input
            v-model="Symmetry"
            type="number"
            placeholder="Simetría"
          />
          <b-form-input
            v-model="FractalDimension"
            type="number"
            placeholder="Dimensión Fractal"
          />
        </b-row>

        <b-row align-v="center">
          <b-button
            :disabled="!file"
            class="mt-2"
            variant="primary"
            block
            @click="readFile"
          >
            Upload
          </b-button>
          <div v-if="error" class="text-danger small ml-2">
            {{ error }}
          </div>
        </b-row>
        <b-row>
          <b-button
            :disabled="!file"
            class="mt-2"
            variant="danger"
            block
            @click="clearData"
          >
            Clear
          </b-button>
        </b-row>
      </b-col>
    </b-row>

    <b-col cols="9">
      <b-table striped hover :items="data" :busy="loading" responsive>
        <template #table-busy>
          <div class="text-center text-danger my-2">
            <b-spinner class="align-middle"></b-spinner>
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>
    </b-col>

    <b-row>
      <b-col cols="14">
        <b-img v-if="graphImg" :src="graphImg" fluid />
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="10">
        <b-table striped hover :items="data2" :busy="loading" responsive>
          <template #table-busy>
            <div class="text-center text-danger my-2">
              <b-spinner class="align-middle"></b-spinner>
              <strong>Loading...</strong>
            </div>
          </template>
        </b-table>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="12">
        <b-img v-if="graphImg2" :src="graphImg2" fluid />
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="12">
        <p v-if="graphImg3" class="font-weight-bold" style="color: red">
          - Mapa de Calor -
        </p>
        <b-img v-if="graphImg3" :src="graphImg3" fluid />
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="9">
        <b-table striped hover :items="data3" :busy="loading" responsive>
          <template #table-busy>
            <div class="text-center text-danger my-2">
              <b-spinner class="align-middle"></b-spinner>
              <strong>Loading...</strong>
            </div>
          </template>
        </b-table>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="3">
        <b-table striped hover :items="data4" :busy="loading" responsive>
          <template #table-busy>
            <div class="text-center text-danger my-2">
              <b-spinner class="align-middle"></b-spinner>
              <strong>Loading...</strong>
            </div>
          </template>
        </b-table>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="9">
        <b-table striped hover :items="data5" :busy="loading" responsive>
          <template #table-busy>
            <div class="text-center text-danger my-2">
              <b-spinner class="align-middle"></b-spinner>
              <strong>Loading...</strong>
            </div>
          </template>
        </b-table>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="10">
        <b-img v-if="graphImg4" :src="graphImg4" fluid />
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="2">
        <b-table striped hover :items="data6" :busy="loading" responsive>
          <template #table-busy>
            <div class="text-center text-danger my-2">
              <b-spinner class="align-middle"></b-spinner>
              <strong>Loading...</strong>
            </div>
          </template>
        </b-table>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="5">
        <b-table striped hover :items="data7" :busy="loading" responsive>
          <template #table-busy>
            <div class="text-center text-danger my-2">
              <b-spinner class="align-middle"></b-spinner>
              <strong>Loading...</strong>
            </div>
          </template>
        </b-table>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="3">
        <b-table striped hover :items="data8" :busy="loading" responsive>
          <template #table-busy>
            <div class="text-center text-danger my-2">
              <b-spinner class="align-middle"></b-spinner>
              <strong>Loading...</strong>
            </div>
          </template>
        </b-table>
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="3">
        <b-table striped hover :items="data9" :busy="loading" responsive>
          <template #table-busy>
            <div class="text-center text-danger my-2">
              <b-spinner class="align-middle"></b-spinner>
              <strong>Loading...</strong>
            </div>
          </template>
        </b-table>
      </b-col>
    </b-row>

    <b-row v-if="graphImg">
      <b-col cols="12">
        <b-alert variant="danger" :show="resultado == 0"
          ><span class="font-weight-bold">Resultado del nuevo pronostico: </span
          >MALIGNO</b-alert
        >
        <b-alert variant="success" :show="resultado == 1"
          ><span class="font-weight-bold">Resultado del nuevo pronostico: </span
          >Benigno</b-alert
        >
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: 'FileReader8',
  data() {
    return {
      file: null,
      data: [],
      data2: [],
      data3: [],
      data4: [],
      data5: [],
      data6: [],
      data7: [],
      data8: [],
      data9: [],
      resultado: [],
      loading: false,
      error: null,
      graphImg: null,
      graphImg2: null,
      graphImg3: null,
      graphImg4: null,
      variableEvalCRL: null,
      porcentajeCRL: null,
      Texture: null,
      Perimeter: null,
      Smoothness: null,
      Compactness: null,
      Symmetry: null,
      FractalDimension: null,
    }
  },
  methods: {
    async readFile() {
      this.loading = true
      this.error = null
      this.graphImg = null
      this.graphImg2 = null
      this.graphImg3 = null
      this.graphImg4 = null
      try {
        const formData = new FormData()
        formData.append('file', this.$refs.file.files[0])
        formData.append('variableEvalCRL', this.variableEvalCRL)
        formData.append('porcentajeCRL', this.porcentajeCRL)
        formData.append('Texture', this.Texture)
        formData.append('Perimeter', this.Perimeter)
        formData.append('Smoothness', this.Smoothness)
        formData.append('Compactness', this.Compactness)
        formData.append('Symmetry', this.Symmetry)
        formData.append('FractalDimension', this.FractalDimension)

        const response = await this.$axios.$post(
          '/clasificacionRegresionLogistica',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }
        )

        this.data = JSON.parse(response.data)
        this.data2 = JSON.parse(response.data2)
        this.data3 = JSON.parse(response.data3)
        this.data4 = JSON.parse(response.data4)
        this.data5 = JSON.parse(response.data5)
        this.data6 = JSON.parse(response.data6)
        this.data7 = JSON.parse(response.data7)
        this.data8 = JSON.parse(response.data8)
        this.data9 = JSON.parse(response.data9)
        this.resultado = JSON.parse(response.newpronostico2)

        this.graphImg = this.$axios.defaults.baseURL + '/' + response.graph
        this.graphImg2 = this.$axios.defaults.baseURL + '/' + response.graph2
        this.graphImg3 = this.$axios.defaults.baseURL + '/' + response.imgcalor
        this.graphImg4 = this.$axios.defaults.baseURL + '/' + response.graph4
      } catch (error) {
        this.error = error.response.data.message
      } finally {
        this.loading = false
      }
    },
    clearData() {
      this.data = []
      this.data2 = []
      this.data3 = []
      this.data4 = []
      this.data5 = []
      this.data6 = []
      this.data7 = []
      this.data8 = []
      this.data9 = []
      this.graphImg = null
      this.graphImg2 = null
      this.graphImg3 = null
      this.graphImg4 = null
      this.file = null
      this.Texture = null
      this.Perimeter = null
      this.Smoothness = null
      this.Compactness = null
      this.Symmetry = null
      this.FractalDimension = null
      this.resultado = null
    },
  },
}
</script>

<style></style>
