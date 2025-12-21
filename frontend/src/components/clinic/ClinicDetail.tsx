import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { Calendar, Clock, Phone, MapPin, Star, Users } from 'lucide-react';
import { apiClient, API_ENDPOINTS } from '../../api/client';
import { Clinic, Doctor, Service, Review } from '../../types';
import BookingModal from './BookingModal';
import ReviewSection from './ReviewSection';

interface ClinicDetailProps {
  clinicId: string;
}

const ClinicDetail: React.FC = () => {
  const { clinicId } = useParams<{ clinicId: string }>();
  const navigate = useNavigate();
  const [clinic, setClinic] = useState<Clinic | null>(null);
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [services, setServices] = useState<Service[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [activeTab, setActiveTab] = useState<'overview' | 'doctors' | 'services' | 'reviews'>('overview');
  const [isBookingModalOpen, setIsBookingModalOpen] = useState(false);
  const [selectedService, setSelectedService] = useState<Service | null>(null);

  useEffect(() => {
    fetchClinicDetails();
  }, [clinicId]);

  const fetchClinicDetails = async () => {
    try {
      // 获取诊所详情
      const clinicData = await apiClient.get<Clinic>(API_ENDPOINTS.CLINIC_DETAIL(clinicId!));
      setClinic(clinicData);

      // 获取医生列表
      const doctorsData = await apiClient.get<Doctor[]>(API_ENDPOINTS.CLINIC_DOCTORS(clinicId!));
      setDoctors(doctorsData);

      // 获取服务列表
      const servicesData = await apiClient.get<Service[]>(API_ENDPOINTS.CLINIC_SERVICES(clinicId!));
      setServices(servicesData);

      // 获取评价
      const reviewsData = await apiClient.get<Review[]>(API_ENDPOINTS.CLINIC_REVIEWS(clinicId!));
      setReviews(reviewsData);
    } catch (error) {
      console.error('Failed to fetch clinic details:', error);
    }
  };

  const handleBookAppointment = (service: Service) => {
    setSelectedService(service);
    setIsBookingModalOpen(true);
  };

  if (!clinic) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="relative h-96 bg-gradient-to-r from-blue-600 to-teal-500">
        <div className="absolute inset-0 bg-black opacity-40"></div>
        <div className="relative container mx-auto px-4 h-full flex items-center">
          <div className="text-white">
            <h1 className="text-5xl font-bold mb-4">{clinic.name}</h1>
            <p className="text-xl mb-6">{clinic.description}</p>
            <div className="flex items-center space-x-6">
              <div className="flex items-center">
                <Star className="w-5 h-5 mr-2 fill-current" />
                <span className="text-lg">{clinic.rating.toFixed(1)} ({clinic.review_count} 评价)</span>
              </div>
              <div className="flex items-center">
                <MapPin className="w-5 h-5 mr-2" />
                <span className="text-lg">{clinic.address}, {clinic.city}</span>
              </div>
              <div className="flex items-center">
                <Phone className="w-5 h-5 mr-2" />
                <span className="text-lg">{clinic.phone}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Left Column - Tabs */}
          <div className="lg:w-2/3">
            {/* Tabs */}
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8">
                <button
                  onClick={() => setActiveTab('overview')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'overview'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  诊所概览
                </button>
                <button
                  onClick={() => setActiveTab('doctors')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'doctors'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  医生团队
                </button>
                <button
                  onClick={() => setActiveTab('services')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'services'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  服务项目
                </button>
                <button
                  onClick={() => setActiveTab('reviews')}
                  className={`py-4 px-1 border-b-2 font-medium text-sm ${
                    activeTab === 'reviews'
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  患者评价
                </button>
              </nav>
            </div>

            {/* Tab Content */}
            <div className="py-8">
              {activeTab === 'overview' && (
                <div>
                  <h2 className="text-2xl font-bold mb-6">诊所介绍</h2>
                  <p className="text-gray-700 mb-6">{clinic.services_description}</p>
                  
                  {/* 设施 */}
                  {clinic.amenities && clinic.amenities.length > 0 && (
                    <div className="mb-8">
                      <h3 className="text-xl font-semibold mb-4">设施与服务</h3>
                      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                        {clinic.amenities.map((amenity, index) => (
                          <div key={index} className="flex items-center">
                            <div className="w-2 h-2 bg-blue-500 rounded-full mr-2"></div>
                            <span>{amenity}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* 地图 */}
                  {clinic.latitude && clinic.longitude && (
                    <div className="mt-8">
                      <h3 className="text-xl font-semibold mb-4">位置</h3>
                      <div className="h-96 rounded-lg overflow-hidden">
                        <MapContainer
                          center={[clinic.latitude, clinic.longitude]}
                          zoom={15}
                          className="h-full w-full"
                        >
                          <TileLayer
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                          />
                          <Marker position={[clinic.latitude, clinic.longitude]}>
                            <Popup>{clinic.name}</Popup>
                          </Marker>
                        </MapContainer>
                      </div>
                    </div>
                  )}
                </div>
              )}

              {activeTab === 'doctors' && (
                <div>
                  <h2 className="text-2xl font-bold mb-6">医生团队</h2>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {doctors.map((doctor) => (
                      <div key={doctor.id} className="bg-white rounded-lg shadow-md p-6">
                        <div className="flex items-start">
                          {doctor.photo_url ? (
                            <img
                              src={doctor.photo_url}
                              alt={doctor.name}
                              className="w-24 h-24 rounded-full object-cover mr-6"
                            />
                          ) : (
                            <div className="w-24 h-24 rounded-full bg-gray-200 flex items-center justify-center mr-6">
                              <Users className="w-12 h-12 text-gray-400" />
                            </div>
                          )}
                          <div>
                            <h3 className="text-xl font-semibold">{doctor.name}</h3>
                            <p className="text-gray-600 mb-2">{doctor.title}</p>
                            <p className="text-gray-700 mb-2">{doctor.specialization}</p>
                            <div className="flex items-center mb-2">
                              <Clock className="w-4 h-4 mr-2 text-gray-500" />
                              <span>{doctor.experience_years} 年经验</span>
                            </div>
                            {doctor.languages && doctor.languages.length > 0 && (
                              <div className="flex flex-wrap gap-2">
                                {doctor.languages.map((lang, index) => (
                                  <span
                                    key={index}
                                    className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full"
                                  >
                                    {lang}
                                  </span>
                                ))}
                              </div>
                            )}
                          </div>
                        </div>
                        {doctor.bio && (
                          <p className="mt-4 text-gray-700">{doctor.bio}</p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === 'services' && (
                <div>
                  <h2 className="text-2xl font-bold mb-6">服务项目</h2>
                  <div className="grid grid-cols-1 gap-6">
                    {services.map((service) => (
                      <div key={service.id} className="bg-white rounded-lg shadow-md p-6">
                        <div className="flex justify-between items-start">
                          <div>
                            <h3 className="text-xl font-semibold mb-2">{service.name}</h3>
                            {service.description && (
                              <p className="text-gray-700 mb-4">{service.description}</p>
                            )}
                            <div className="flex items-center space-x-4">
                              <div className="flex items-center">
                                <Clock className="w-4 h-4 mr-2 text-gray-500" />
                                <span>{service.duration} 分钟</span>
                              </div>
                              <div className="flex items-center">
                                <span className="text-2xl font-bold text-blue-600">
                                  ${service.price.toFixed(2)}
                                </span>
                              </div>
                            </div>
                          </div>
                          <button
                            onClick={() => handleBookAppointment(service)}
                            className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
                          >
                            立即预约
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {activeTab === 'reviews' && (
                <ReviewSection reviews={reviews} clinicId={clinicId!} />
              )}
            </div>
          </div>

          {/* Right Column - Booking Card */}
          <div className="lg:w-1/3">
            <div className="sticky top-8 bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-2xl font-bold mb-6">立即预约</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    选择服务
                  </label>
                  <select
                    className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    onChange={(e) => {
                      const service = services.find(s => s.id === e.target.value);
                      if (service) handleBookAppointment(service);
                    }}
                  >
                    <option value="">请选择服务项目</option>
                    {services.map((service) => (
                      <option key={service.id} value={service.id}>
                        {service.name} - ${service.price.toFixed(2)}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div className="pt-4 border-t border-gray-200">
                  <h4 className="font-semibold mb-2">营业时间</h4>
                  <p className="text-gray-600">周一至周五: 9:00 AM - 6:00 PM</p>
                  <p className="text-gray-600">周六: 10:00 AM - 4:00 PM</p>
                  <p className="text-gray-600">周日: 休息</p>
                </div>
                
                <div className="pt-4 border-t border-gray-200">
                  <h4 className="font-semibold mb-2">联系方式</h4>
                  <p className="text-gray-600 flex items-center">
                    <Phone className="w-4 h-4 mr-2" />
                    {clinic.phone}
                  </p>
                  <p className="text-gray-600">{clinic.email}</p>
                </div>
                
                <button
                  onClick={() => navigate(`/clinics/${clinicId}/booking`)}
                  className="w-full mt-6 py-3 bg-gradient-to-r from-blue-600 to-teal-500 text-white font-semibold rounded-lg hover:opacity-90 transition-opacity"
                >
                  查看可用时间
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Booking Modal */}
      {isBookingModalOpen && selectedService && (
        <BookingModal
          clinic={clinic}
          service={selectedService}
          doctors={doctors}
          isOpen={isBookingModalOpen}
          onClose={() => {
            setIsBookingModalOpen(false);
            setSelectedService(null);
          }}
        />
      )}
    </div>
  );
};

export default ClinicDetail;