<template>
  <b-container>
    <b-row align-h="center">
      <b-col cols="12" md="8" lg="9" class="text-center">
        <b-img src="@/assets/logo.png" fluid></b-img>
      </b-col>
    </b-row>
    <h1 class="row justify-content-center">
      Clasificación <small> Árbol de Decisión</small>
    </h1>
    <b-row class="my-4" align-h="center">
      <b-col cols="3">
        <b-row>
          <b-form-file ref="file" v-model="file" />

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

    <b-col cols="15">
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
      <b-col cols="12">
        <p v-if="graphImg3" class="font-weight-bold" style="color: red">
          - Mapa de Calor -
        </p>
        <b-img v-if="graphImg3" :src="graphImg3" fluid />
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="13">
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
      <b-col cols="11">
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
      <b-col cols="10">
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
      <b-col cols="10">
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
      <b-col cols="5">
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

    <b-row>
      <b-col cols="13">
        <b-img v-if="graphImg" :src="graphImg" fluid />
      </b-col>
    </b-row>

    <b-row>
      <b-col cols="5">
        <b-table striped hover :items="data10" :busy="loading" responsive>
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
      <iframe
        src="http://localhost:5000/static/documentos/generados/arbolito12.pdf"
        width="600"
        height="780"
        style="border: none"
      ></iframe>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: 'FileReader7',
  data() {
    return {
      file: null,
      data: [],
      data2: [],
      data3: [],
      data4: [],
      data5: [],
      data9: [],
      data10: [],
      loading: false,
      error: null,
      graphImg: null,
      graphImg3: null,
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
      this.graphImg3 = null

      try {
        const formData = new FormData()
        formData.append('file', this.$refs.file.files[0])
        formData.append('Texture', this.Texture)
        formData.append('Perimeter', this.Perimeter)
        formData.append('Smoothness', this.Smoothness)
        formData.append('Compactness', this.Compactness)
        formData.append('Symmetry', this.Symmetry)
        formData.append('FractalDimension', this.FractalDimension)
        const response = await this.$axios.$post(
          '/clasificacionArbol',
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
        this.data9 = JSON.parse(response.data9)
        this.data10 = JSON.parse(response.data10)


        this.graphImg = this.$axios.defaults.baseURL + '/' + response.graph
        this.graphImg3 = this.$axios.defaults.baseURL + '/' + response.imgcalor
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
      this.data9 = []
      this.data10 = []
      this.graphImg = null
      this.graphImg3 = null
      this.file = null
      this.Texture = null
      this.Perimeter = null
      this.Smoothness = null
      this.Compactness = null
      this.Symmetry = null
      this.FractalDimension = null

    },
  },
}
</script>

<style></style>
